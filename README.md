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

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   ```
   http://localhost:5000
   ```

4. **Explore!**
   - Use the time slider to travel through history (3000 BCE to present)
   - Click anywhere on the map
   - See what was happening at that location and time

## 📖 How It Works (Right Now)

**Current Version (v0.1 - "Proof of Concept"):**
- Simple 2D world map (Leaflet.js)
- Time slider from 3000 BCE to 2024 CE
- Click any location → finds nearest major city
- Fetches Wikipedia info for that location
- Shows information in knowledge categories
- Displays confidence score (how much we know)

**What's Next:**
- Better location detection (not just major cities)
- Improved historical information extraction
- Add more knowledge categories
- Better confidence scoring
- Cache results (SQLite)
- More beautiful UI

## 🏗️ Project Structure

```
continuum/
├── app.py              # Flask server (main backend)
├── templates/
│   └── index.html      # Frontend (map + UI)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🛠️ Technology Stack (Simple!)

- **Backend:** Python + Flask (just a simple web server)
- **Frontend:** Plain HTML + CSS + JavaScript (no frameworks!)
- **Map:** Leaflet.js (simple, no React needed)
- **Data:** Wikipedia API (real-time, no database yet)

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

## 🎯 Current Limitations (We'll Fix These!)

1. **Only major cities work well** - clicking random ocean gives nearest city
2. **Wikipedia only** - no specialized historical sources yet
3. **Simple info extraction** - not very smart about categories yet
4. **No caching** - same query hits Wikipedia every time
5. **2D map** - not the 3D globe from your vision yet

**But that's OK!** This is your Day 1. Every improvement from here is progress you can see.

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
