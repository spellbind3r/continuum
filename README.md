# Continuum - Historical World Explorer

An interactive time-traveling world explorer that lets you click anywhere on Earth and discover what was happening at that location in any time period.

## 🚀 Run It TODAY (5 minutes)

### Prerequisites
- Python 3.8 or higher
- pip (comes with Python)

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Populate the knowledge base** (first time only):
   ```bash
   python scripts/populate_all_cities.py
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   ```
   http://localhost:5000
   ```

5. **Explore!**
   - Use the time slider to travel through history (3000 BCE to present)
   - Click on any of the 15 cities on the map
   - See detailed historical information for that period
   - Click "🔄 Dig Deeper" to bypass cache
   - Click "✨ Tell me more!" for AI-enhanced narrative (requires API key)

### ✨ Optional: AI Enhancement Setup

To enable the AI-powered narrative enhancement feature:

1. **Get an Anthropic API key:**
   - Sign up at https://console.anthropic.com/
   - Get your API key from the dashboard

2. **Create a `.env` file** in the project root:
   ```bash
   cp .env.example .env
   ```

3. **Add your API key** to `.env`:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

4. **Restart the app** and look for this message:
   ```
   [LLM] Anthropic integration enabled with model: claude-3-5-sonnet-20241022
   ```

5. **Use the feature:**
   - Click on a city and time period
   - The "✨ Tell me more!" button will appear
   - Click it to get an AI-generated narrative that brings the period to life

**Note:** The AI enhancement feature is completely optional. The app works great without it using the curated knowledge base!

## 📖 How It Works (Right Now)

**Current Version (v0.4.0-globe - "3D Globe with Historical Boundaries"):**
- **15 Cities Covered:** Rome, Athens, Cairo, Baghdad, Beijing, London, Paris, Delhi, Istanbul, Venice, Kyiv, Jerusalem, Xi'an, Mexico City, Cuzco
- **56 Historical Periods:** From 3100 BCE to 1920 CE with detailed period-specific information
- **Knowledge Base:** Structured historical data with Politics, Culture, Religion categories
- **🌍 3D Globe View (NEW!):** Toggle between 2D map and interactive 3D globe with topography
- **⚔️ Historical Boundaries (NEW!):** See kingdoms, empires, and regions change as you move through time
  - 30+ historical entities: Roman Empire, Persian Empire, Chinese Dynasties, Islamic Caliphates, and more
  - Boundaries automatically update as you move the time slider
  - Click polygons to see kingdom details (name, type, period, capital)
- **Smart Time Slider:** Logarithmic scale (more detail for recent history)
- **Caching System:** Fast response times with SQLite cache
- **"Dig Deeper" Feature:** Bypass cache for fresh knowledge base queries
- **✨ AI Enhancement:** Optional LLM-powered narrative enhancement for richer storytelling
- **Layer Controls:** Toggle different historical layers (kingdoms active, languages/religions coming soon)
- **Debug Panel:** Transparent view of data sources and request flow

**What's Next:**
- Language distribution maps (historical linguistics)
- Religion spread visualization
- Visual timeline display for each city
- Connections/trade routes between cities at same time period
- More cities and historical periods
- Year-specific events
- Advanced LLM features (comparative analysis, natural language queries)

## 🏗️ Project Structure

```
continuum/
├── app.py                          # Flask server (main backend with LLM integration)
├── templates/
│   └── index.html                  # Frontend (2D map + 3D globe + UI)
├── static/
│   └── js/
│       └── historical_boundaries.js # Historical kingdoms/empires data (30+ entities)
├── scripts/
│   ├── populate_all_cities.py      # Populate knowledge base with all 15 cities
│   ├── populate_sample_data.py     # Populate sample data (Rome only)
│   └── test_all_cities.py          # Automated quality tests for all cities
├── continuum_knowledge.db          # Knowledge base (created by populate script)
├── continuum_cache.db              # Query cache (created automatically)
├── .env                            # Environment variables (create from .env.example)
├── .env.example                    # Template for environment variables
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── CITIES_COVERAGE.md              # Detailed list of all historical periods
├── NEXT_STEPS.md                   # Development roadmap
└── CLAUDE.md                       # AI assistant development guide
```

## 🛠️ Technology Stack

- **Backend:** Python + Flask
- **Frontend:** Plain HTML + CSS + JavaScript (no frameworks!)
- **Visualization:**
  - **2D Map:** Leaflet.js (interactive flat map)
  - **3D Globe:** Globe.gl + Three.js (WebGL globe with topography)
- **Database:** SQLite (knowledge base + cache)
- **AI/LLM:** Anthropic Claude API (optional enhancement)
- **Data Sources:**
  - Curated knowledge base (56 historical periods)
  - Historical boundaries dataset (30+ kingdoms/empires)
  - Wikipedia API (fallback for uncovered periods)
  - Claude AI (optional narrative enhancement)

## 💡 Your Learning Path

**Phase 0 (TODAY):** ✅ You are here!
- Get something working
- See the concept come to life
- Click and explore

**Phase 1 (Tomorrow+):**
- Add SQLite to cache results
- Improve location detection
- Better information extraction
- More knowledge categories

**Phase 2 (Next Week+):**
- Add actual historical maps
- Show borders changing over time
- Better confidence visualization
- "I don't know" messaging

**Phase 3 (Future):**
- 3D globe (upgrade from 2D map)
- Find connections between places
- Timeline visualization
- Much richer data

## 🎯 Current Scope & Limitations

**What Works Great:**
- ✅ 15 major cities with rich historical data
- ✅ 56 historical periods (3100 BCE to 1920 CE)
- ✅ 3D globe with topography and historical boundaries
- ✅ 30+ historical kingdoms/empires visualized
- ✅ Fast caching system
- ✅ Debug panel for transparency
- ✅ Optional AI enhancement

**Known Limitations:**
1. **Limited cities** - Only 15 cities currently have detailed historical data
2. **Coverage gaps** - Modern periods (after 1920) fall back to Wikipedia
3. **City-centric** - Clicking outside cities finds nearest major city
4. **Simplified boundaries** - Historical borders are approximate rectangles/polygons (GeaCron-quality data planned)
5. **Kingdoms only** - Language and religion layers are placeholders (coming soon)
6. **LLM costs** - AI enhancement requires API key and has usage costs

**But that's OK!** Every query is transparent about its source and confidence level.

## 🔧 Customizing

Want to tweak something? Here's where to look:

- **Change cities:** Edit `get_nearest_city()` in `app.py`
- **Change time range:** Edit `min="-3000" max="2024"` in `index.html`
- **Change colors:** Edit the `<style>` section in `index.html`
- **Add categories:** Edit `fetch_historical_info()` in `app.py`

## 🐛 Troubleshooting

**"Port 5000 already in use"**
```bash
python app.py --port 5001
```

Or edit `app.py` and change `port=5000` to `port=5001`

**"Module not found"**
```bash
pip install -r requirements.txt
```

**No internet / Wikipedia slow**
The app needs internet to fetch Wikipedia data. That's why we'll add caching in Phase 1!

## 📚 Next Steps

1. **Play with it!** Click around, try different times
2. **Show someone!** Share your screen, get feedback
3. **Pick one improvement** from the list above
4. **Make it yours!** Change colors, add cities, experiment

## 🎓 Learning Resources (For When You're Ready)

- **Flask basics:** https://flask.palletsprojects.com/quickstart/
- **Leaflet map:** https://leafletjs.com/examples.html
- **Wikipedia API:** https://pypi.org/project/Wikipedia-API/
- **HTML/CSS/JS:** https://www.w3schools.com/

---

**Remember:** This is a learning journey. Every small improvement is a win. Don't try to build everything at once. Build, learn, iterate! 🚀
