from flask import Flask, render_template, jsonify, request
import wikipediaapi
import sqlite3
import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

app = Flask(__name__)
wiki = wikipediaapi.Wikipedia('Continuum/1.0 (contact@example.com)', 'en')

# Get the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize Anthropic client (if API key is available)
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
ENABLE_LLM = os.getenv('ENABLE_LLM', 'true').lower() == 'true' and ANTHROPIC_API_KEY

if ENABLE_LLM:
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
    print(f"[LLM] Anthropic integration enabled with model: {ANTHROPIC_MODEL}")
else:
    anthropic_client = None
    print("[LLM] Anthropic integration disabled (no API key found)")

# Database setup - use absolute paths
DB_PATH = os.path.join(BASE_DIR, 'continuum_cache.db')
KB_DB_PATH = os.path.join(BASE_DIR, 'continuum_knowledge.db')

# Version number (from git commits)
VERSION = 'v0.3.0-llm'  # LLM integration for enhanced narratives

def init_db():
    """Initialize SQLite database for caching"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS wikipedia_cache (
            location TEXT,
            year INTEGER,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (location, year)
        )
    ''')
    conn.commit()
    conn.close()

def get_cached_data(location, year):
    """Retrieve cached data from database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT data FROM wikipedia_cache WHERE location = ? AND year = ?',
              (location, year))
    result = c.fetchone()
    conn.close()

    if result:
        return json.loads(result[0])
    return None

def cache_data(location, year, data):
    """Store data in cache"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO wikipedia_cache (location, year, data)
        VALUES (?, ?, ?)
    ''', (location, year, json.dumps(data)))
    conn.commit()
    conn.close()

# Knowledge base functions
def query_knowledge_base(location, year):
    """Query structured knowledge base for period-specific information"""
    print(f"[KB Query] Called with location='{location}', year={year}")
    print(f"[KB Query] KB_DB_PATH='{KB_DB_PATH}'")
    print(f"[KB Query] Path exists: {os.path.exists(KB_DB_PATH)}")

    if not os.path.exists(KB_DB_PATH):
        print(f"[KB Query] ERROR: KB file doesn't exist!")
        return None

    try:
        conn = sqlite3.connect(KB_DB_PATH)
        c = conn.cursor()

        # Find the period this year falls into
        c.execute('''
            SELECT id, period_name, description, source_page
            FROM historical_periods
            WHERE location = ?
              AND start_year <= ?
              AND end_year >= ?
            LIMIT 1
        ''', (location, year, year))

        period = c.fetchone()

        if not period:
            print(f"[KB Query] No period found for {location} at year {year}")
            conn.close()
            return None

        print(f"[KB Query] Found period: {period[1]}")

        period_id, period_name, description, source_page = period

        # Get facts for this period
        c.execute('''
            SELECT category, content, confidence
            FROM period_facts
            WHERE period_id = ?
        ''', (period_id,))

        facts = c.fetchall()
        conn.close()

        # Structure the response
        categories = {}
        for category, content, confidence in facts:
            categories[category] = {
                'content': content,
                'confidence': confidence
            }

        # Add default categories if missing
        if 'overview' not in categories and description:
            categories['overview'] = {
                'content': description,
                'confidence': 0.85
            }

        result = {
            'location': location,
            'year': year,
            'period': period_name,
            'categories': categories if categories else None,
            'source': 'knowledge_base',
            'source_page': source_page
        }

        print(f"[KB Query] Returning result with {len(categories)} categories")
        return result

    except sqlite3.Error as e:
        print(f"[KB Query] ERROR: {e}")
        return None

def enhance_with_llm(location, year, kb_data):
    """Enhance knowledge base data with LLM-generated insights"""
    if not ENABLE_LLM or not anthropic_client:
        print("[LLM] Enhancement not available (LLM disabled or no API key)")
        return None

    try:
        print(f"[LLM] Enhancing data for {location} at year {year}")

        # Build context from knowledge base data
        period_name = kb_data.get('period', 'Unknown Period')
        categories = kb_data.get('categories', {})

        # Extract category content for context
        context_parts = [f"Historical Period: {period_name}", f"Location: {location}", f"Year: {year}", ""]

        for category, data in categories.items():
            if isinstance(data, dict) and 'content' in data:
                context_parts.append(f"{category.upper()}: {data['content']}")

        context = "\n\n".join(context_parts)

        # Create prompt for LLM
        prompt = f"""Based on the following historical information, provide additional engaging insights and context that would help someone understand what life was like in {location} around the year {year}.

{context}

Please provide:
1. A vivid narrative description (2-3 paragraphs) that brings this period to life
2. Notable figures or events from this specific time
3. Daily life details (what people ate, wore, how they lived)
4. Interesting lesser-known facts that aren't in the basic overview

Write in an engaging, educational style that captures the wonder of this historical period. Be specific to the year range when possible."""

        # Call Anthropic API
        message = anthropic_client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1500,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        llm_response = message.content[0].text

        print(f"[LLM] Successfully generated {len(llm_response)} characters of enhanced content")

        # Structure the enhanced response
        enhanced_data = {
            'location': location,
            'year': year,
            'period': period_name,
            'categories': categories,  # Keep original KB categories
            'enhanced_narrative': {
                'content': llm_response,
                'confidence': 0.75,  # LLM content is well-informed but not primary source
                'source': 'llm_enhanced'
            },
            'source': 'knowledge_base_with_llm_enhancement',
            'source_page': kb_data.get('source_page'),
            'llm_model': ANTHROPIC_MODEL
        }

        return enhanced_data

    except Exception as e:
        print(f"[LLM] ERROR during enhancement: {e}")
        return None

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html', version=VERSION)

@app.route('/version')
def version():
    """Return current version"""
    return jsonify({'version': VERSION})

@app.route('/explore', methods=['POST'])
def explore():
    """Get historical information for a location and time period"""
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    year = data.get('year', 2024)
    bypass_cache = data.get('bypass_cache', False)
    use_llm = data.get('use_llm', False)  # New parameter for LLM enhancement

    # Simple geocoding - map coordinates to known cities (for demo)
    location_name = get_nearest_city(lat, lng)

    # Check cache first (unless bypassing)
    if not bypass_cache and not use_llm:  # Don't use cache for LLM requests
        cached_info = get_cached_data(location_name, year)
        if cached_info:
            cached_info['from_cache'] = True
            cached_info['debug_info'] = {
                'source_order': ['cache'],
                'cache_hit': True,
                'llm_available': ENABLE_LLM
            }
            return jsonify(cached_info)

    # Try knowledge base first
    kb_info = query_knowledge_base(location_name, year)

    if kb_info and kb_info.get('categories'):
        # If LLM enhancement is requested and available
        if use_llm and ENABLE_LLM:
            enhanced_info = enhance_with_llm(location_name, year, kb_info)

            if enhanced_info:
                enhanced_info['from_cache'] = False
                enhanced_info['debug_info'] = {
                    'source_order': ['cache (bypassed)', 'knowledge_base', 'llm_enhancement'],
                    'knowledge_base_hit': True,
                    'llm_enhanced': True,
                    'cache_bypassed': True,
                    'period': enhanced_info.get('period'),
                    'source_page': enhanced_info.get('source_page'),
                    'llm_model': ANTHROPIC_MODEL
                }
                # Don't cache LLM responses (expensive and may vary)
                return jsonify(enhanced_info)

        # Knowledge base has data for this period (standard response)
        kb_info['from_cache'] = False
        kb_info['debug_info'] = {
            'source_order': ['cache (bypassed)', 'knowledge_base'] if bypass_cache else ['knowledge_base'],
            'knowledge_base_hit': True,
            'cache_bypassed': bypass_cache,
            'period': kb_info.get('period'),
            'source_page': kb_info.get('source_page'),
            'llm_available': ENABLE_LLM
        }

        # Cache the knowledge base result (but not LLM enhanced)
        cache_data(location_name, year, kb_info)
        return jsonify(kb_info)

    # Fallback to Wikipedia API
    wiki_info = fetch_historical_info(location_name, year)
    wiki_info['from_cache'] = False
    wiki_info['debug_info'] = {
        'source_order': ['cache (bypassed)', 'knowledge_base', 'wikipedia_api'] if bypass_cache else ['knowledge_base', 'wikipedia_api'],
        'knowledge_base_hit': False,
        'wikipedia_api_hit': True,
        'cache_bypassed': bypass_cache
    }

    # Cache the result
    cache_data(location_name, year, wiki_info)

    return jsonify(wiki_info)

def get_nearest_city(lat, lng):
    """Simple mapping of coordinates to major cities"""
    cities = {
        'Rome': (41.9, 12.5),
        'Athens': (37.9, 23.7),
        'Cairo': (30.0, 31.2),
        'Baghdad': (33.3, 44.4),
        'Beijing': (39.9, 116.4),
        'London': (51.5, -0.1),
        'Paris': (48.9, 2.4),
        'Delhi': (28.6, 77.2),
        'Istanbul': (41.0, 28.9),
        'Venice': (45.4, 12.3),
        'Kyiv': (50.5, 30.5),
        'Jerusalem': (31.8, 35.2),
        "Xi'an": (34.3, 108.9),
        'Mexico City': (19.4, -99.1),
        'Cuzco': (-13.5, -71.9),
    }

    # Find closest city (simple distance calc)
    min_dist = float('inf')
    closest = 'Rome'

    for city, (city_lat, city_lng) in cities.items():
        dist = ((lat - city_lat)**2 + (lng - city_lng)**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest = city

    return closest

def fetch_historical_info(location, year):
    """Fetch historical information from Wikipedia"""

    # Try to find relevant Wikipedia page
    search_terms = [
        f"{location}",
        f"History of {location}",
        f"{location} in the {get_century(year)}"
    ]

    page_content = ""
    confidence = 0.3

    for term in search_terms:
        page = wiki.page(term)
        if page.exists():
            page_content = page.summary[:500]  # First 500 chars
            confidence = min(0.9, 0.5 + len(page.summary) / 2000)
            break

    if not page_content:
        page_content = f"Limited historical information available for {location} around {year}."
        confidence = 0.1

    # Structure into knowledge categories (simplified for demo)
    return {
        'location': location,
        'year': year,
        'confidence': confidence,
        'categories': {
            'overview': {
                'content': page_content,
                'confidence': confidence
            },
            'politics': {
                'content': extract_category_hint(page_content, ['government', 'rule', 'empire', 'kingdom']),
                'confidence': confidence * 0.8
            },
            'culture': {
                'content': extract_category_hint(page_content, ['culture', 'art', 'language', 'literature']),
                'confidence': confidence * 0.7
            },
            'religion': {
                'content': extract_category_hint(page_content, ['religion', 'temple', 'church', 'belief']),
                'confidence': confidence * 0.6
            }
        }
    }

def get_century(year):
    """Convert year to century name"""
    if year < 0:
        century = abs(year) // 100 + 1
        return f"{century}th century BCE"
    else:
        century = year // 100 + 1
        return f"{century}th century CE"

def extract_category_hint(text, keywords):
    """Simple keyword-based extraction"""
    sentences = text.split('.')
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            return sentence.strip() + '.'
    return "Information not readily available."

if __name__ == '__main__':
    app.run(debug=True, port=5000)
