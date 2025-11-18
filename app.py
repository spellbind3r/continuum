from flask import Flask, render_template, jsonify, request
import wikipediaapi
import random

app = Flask(__name__)
wiki = wikipediaapi.Wikipedia('Continuum/1.0 (contact@example.com)', 'en')

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

    # Simple geocoding - map coordinates to known cities (for demo)
    location_name = get_nearest_city(lat, lng)

    # Fetch Wikipedia info
    info = fetch_historical_info(location_name, year)

    return jsonify(info)

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
