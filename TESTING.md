# Testing the Hybrid Knowledge Base System

This guide shows you how to test the new knowledge base system with the debug panel.

## Quick Start

1. **Start the app:**
   ```bash
   python app.py
   ```

2. **Open in browser:**
   ```
   http://localhost:5000
   ```

3. **Enable debug panel:**
   - Click the "🔧 Debug" button in the bottom-right corner
   - This shows the data source for each query

## What to Test

### Test 1: Knowledge Base Query (Rome)

**Goal:** Verify the knowledge base provides period-specific information

1. **Click on Rome** (center of Italy on the map)
2. **Slide to different time periods:**
   - **600 BC** → Should show "Roman Kingdom"
   - **100 BC** → Should show "Roman Republic"
   - **200 AD** → Should show "Roman Empire"
   - **1000 AD** → Should show "Medieval Rome"
   - **1500 AD** → Should show "Renaissance Rome"

3. **Check the debug panel:**
   - Data Source should show: `knowledge_base`
   - Historical Period should match the slider
   - Source Page should show: `Timeline of Rome`
   - Load time should be fast (<50ms after first query)

4. **Verify categories:**
   - Should see 4 categories: Overview, Politics, Culture, Religion
   - Each should have period-specific content (not generic)
   - Confidence should be ~85%

### Test 2: Wikipedia Fallback (Athens)

**Goal:** Verify fallback to Wikipedia API when knowledge base has no data

1. **Click on Athens** (Greece)
2. **Check the debug panel:**
   - Data Source should show: `knowledge_base → wikipedia_api`
   - This means knowledge base had no data, fell back to Wikipedia
   - Load time will be slower (~500-2000ms on first query)

3. **Note:** Wikipedia API may be blocked in some environments
   - If you see "Limited historical information available" - that's expected
   - The system tried Wikipedia but couldn't access it
   - This demonstrates graceful degradation

### Test 3: Cache Performance

**Goal:** Verify caching speeds up repeated queries

1. **Click Rome at 100 BC**
   - Note the load time (e.g., 45ms)

2. **Click elsewhere, then click Rome at 100 BC again**
   - Debug panel should show: `cache` as data source
   - Cache badge should show: ⚡ Cached
   - Load time should be ~10-20ms

3. **Change year to 200 AD (new query)**
   - First time: reads from knowledge base (~40ms)
   - Second time: reads from cache (~15ms)

### Test 4: F12 Console Inspection

**Goal:** See detailed request/response data

1. **Open browser developer tools** (F12)
2. **Open Console tab**
3. **Click on Rome**
4. **Look for:** `🔍 Continuum Debug Info`
   - Expand to see full request/response JSON
   - Verify `debug_info` object shows data source hierarchy
   - Check `categories` object has all fields

## Expected Results

### ✅ Working Knowledge Base

When clicking Rome at different years:
- Different historical periods show up
- Content changes based on time period
- Politics/Culture/Religion are period-specific
- Debug shows `knowledge_base` as source

**Example for 100 BC (Roman Republic):**
```
Politics: "Government by Senate and elected consuls. Major expansion..."
Culture: "Golden age of Latin literature with Cicero, Caesar, and Virgil..."
Religion: "Traditional Roman religion flourished. Major temples..."
```

**Example for 200 AD (Roman Empire):**
```
Politics: "Imperial rule under emperors. Peak expansion under Trajan..."
Culture: "Flourishing arts, architecture (Colosseum, Pantheon)..."
Religion: "Traditional Roman religion initially, then gradual spread of Christianity..."
```

### ✅ Working Cache

- First query: ~40-50ms
- Repeated query: ~10-20ms
- Cache badge shows ⚡ Cached
- Debug shows `cache` as first source

### ✅ Working Fallback

For cities without knowledge base data (Athens, Baghdad, etc.):
- Still shows information (from Wikipedia API if accessible)
- Debug shows `knowledge_base → wikipedia_api`
- Gracefully handles Wikipedia API failures

## Troubleshooting

### No data showing for Rome

1. **Check database exists:**
   ```bash
   ls -lh continuum_knowledge.db
   ```
   Should be ~32KB or larger

2. **Repopulate sample data:**
   ```bash
   python scripts/populate_sample_data.py
   ```

### Debug panel not appearing

1. **Check for JavaScript errors** in F12 Console
2. **Refresh the page** (Ctrl+R or Cmd+R)
3. **Clear browser cache** and reload

### "Limited information available" for all cities

- Wikipedia API may be blocked in your network
- Sample data for Rome should still work
- Check debug panel to see which data source failed

## Next Steps

Once you've verified the system works:

1. **Add more cities** to the knowledge base
   - Edit `scripts/build_knowledge_base.py`
   - Add Athens, Baghdad, Beijing, etc.
   - Run the builder when Wikipedia API is accessible

2. **Improve category extraction**
   - Parse Wikipedia timeline sections more intelligently
   - Extract Science, Economy, Diplomacy categories
   - Better confidence scoring based on source quality

3. **Enhance debug panel**
   - Add performance metrics
   - Show cache hit rate
   - Display data quality indicators

---

**Happy exploring through time!** 🌍⏳
