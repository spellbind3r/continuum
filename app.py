from flask import Flask, render_template, jsonify, request
import wikipediaapi
import sqlite3
import json
import os

app = Flask(__name__)
wiki = wikipediaapi.Wikipedia('Continuum/1.0 (contact@example.com)', 'en')

# Database setup
DB_PATH = 'continuum_cache.db'
KB_DB_PATH = 'continuum_knowledge.db'

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
    if not os.path.exists(KB_DB_PATH):
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
            conn.close()
            return None

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

        return {
            'location': location,
            'year': year,
            'period': period_name,
            'categories': categories if categories else None,
            'source': 'knowledge_base',
            'source_page': source_page
        }

    except sqlite3.Error as e:
        print(f"Knowledge base error: {e}")
        return None

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore', methods=['POST'])
def explore():
    """Get historical information for a location and time period"""
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    year = data.get('year', 2024)
    bypass_cache = data.get('bypass_cache', False)

    # Simple geocoding - map coordinates to known cities (for demo)
    location_name = get_nearest_city(lat, lng)

    # Check cache first (unless bypassing)
    if not bypass_cache:
        cached_info = get_cached_data(location_name, year)
        if cached_info:
            cached_info['from_cache'] = True
            cached_info['debug_info'] = {
                'source_order': ['cache'],
                'cache_hit': True
            }
            return jsonify(cached_info)

    # Try knowledge base first
    kb_info = query_knowledge_base(location_name, year)

    if kb_info and kb_info.get('categories'):
        # Knowledge base has data for this period
        kb_info['from_cache'] = False
        kb_info['debug_info'] = {
            'source_order': ['cache (bypassed)', 'knowledge_base'] if bypass_cache else ['knowledge_base'],
            'knowledge_base_hit': True,
            'cache_bypassed': bypass_cache,
            'period': kb_info.get('period'),
            'source_page': kb_info.get('source_page')
        }

        # Cache the knowledge base result
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
