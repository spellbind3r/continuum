# Troubleshooting: Why You're Not Seeing Results

## The Backend IS Working! ✅

I just tested the Flask endpoint directly and it **correctly returns period-specific data**:

```bash
# Test query for Rome at 100 BC
curl -X POST http://localhost:5000/explore \
  -H "Content-Type: application/json" \
  -d '{"lat": 41.9, "lng": 12.5, "year": -100}'

# Returns:
{
  "period": "Roman Republic",
  "categories": {
    "politics": "Government by Senate and elected consuls. Major expansion through Italy and Mediterranean...",
    "culture": "Golden age of Latin literature with Cicero, Caesar, and Virgil...",
    "religion": "Traditional Roman religion flourished. Major temples built to Jupiter, Juno, and Minerva."
  },
  "debug_info": {
    "knowledge_base_hit": true,
    "period": "Roman Republic",
    "source_order": ["knowledge_base"]
  }
}
```

## Why You're Not Seeing Results

### 1. **Only Rome Has Knowledge Base Data**

Currently, **only Rome** has pre-populated historical data covering years **-753 to 1650**:
- Roman Kingdom (-753 to -509)
- Roman Republic (-509 to -27)
- Roman Empire (-27 to 476)
- Medieval Rome (476 to 1420)
- Renaissance Rome (1420 to 1650)

**Delhi, Athens, Baghdad, etc. have NO knowledge base data yet.**

For these cities, the app falls back to Wikipedia API, which is **blocked in this environment**, so you'll see:
> "Limited historical information available for [City]"

### 2. **Rome Only Works for Specific Year Ranges**

If you click Rome but select a year **outside -753 to 1650**, the knowledge base has no data:
- ❌ Year -2000 (2000 BC) - Too ancient, no data
- ❌ Year 1800 - Too recent, no data
- ✅ Year -500 (500 BC) - Roman Kingdom ✓
- ✅ Year -100 (100 BC) - Roman Republic ✓
- ✅ Year 200 (200 AD) - Roman Empire ✓
- ✅ Year 1000 (1000 AD) - Medieval Rome ✓
- ✅ Year 1500 (1500 AD) - Renaissance Rome ✓

### 3. **Browser Cache Issue**

Your browser might be caching the old JavaScript. **Hard refresh:**
- **Windows/Linux**: Ctrl + Shift + R
- **Mac**: Cmd + Shift + R

Or clear browser cache completely.

### 4. **App Might Be Running Old Version**

If you started `python app.py` before the knowledge base was populated, restart it:

```bash
# Kill old Flask process
pkill -f "python app.py"

# Start fresh
python app.py
```

## How to Test Properly

### Step 1: Restart Flask App

```bash
cd /home/user/continuum
python app.py
```

### Step 2: Open Browser

```
http://localhost:5000
```

### Step 3: Test Rome with Good Years

1. **Click on central Italy** (Rome's location)
2. **Move the slider to these positions** (now logarithmic!):
   - **30% position** → Around 100 BCE (Roman Republic)
   - **45% position** → Around 200 CE (Roman Empire)
   - **52% position** → Around 1000 CE (Medieval Rome)
   - **58% position** → Around 1500 CE (Renaissance Rome)

3. **Click the 🔧 Debug button** (bottom-right) to verify:
   - **Data Source** should show: `knowledge_base`
   - **Historical Period** should show the period name
   - **Source Page** should show: `Timeline of Rome`

### Step 4: Watch for Period Changes

As you slide through different years, you should see:
- **Content changes** in Politics, Culture, Religion categories
- **Period name updates** in debug panel
- **Different descriptions** based on time period

## What You Should See

### For Rome at 100 BC (Roman Republic):

**Politics:**
> Government by Senate and elected consuls. Major expansion through Italy and Mediterranean. Conflicts between patricians and plebeians.

**Culture:**
> Golden age of Latin literature with Cicero, Caesar, and Virgil. Development of Roman law and engineering.

**Religion:**
> Traditional Roman religion flourished. Major temples built to Jupiter, Juno, and Minerva.

### For Rome at 1000 AD (Medieval Rome):

**Politics:**
> Papal control with conflicts between Popes and Holy Roman Emperors. Rome became capital of Papal States.

**Culture:**
> Preservation of classical texts in monasteries. Romanesque and Gothic architecture.

**Religion:**
> Center of Catholic Christianity. Construction of major basilicas. Pilgrimage destination.

**Notice:** The content is completely different because it's pulling from the knowledge base for the correct historical period!

## Debug Panel Should Show

When clicking Rome at a valid year:

```
🔍 Debug Information

Request:
  Location: Rome (41.90, 12.50)
  Year: -100

Response:
  Data Source: knowledge_base
  Historical Period: Roman Republic
  Source Page: Timeline of Rome
  Load Time: 25ms
```

## If Still Not Working

### Check 1: Is knowledge base populated?

```bash
ls -lh continuum_knowledge.db
# Should be ~32KB or larger
```

### Check 2: Query database directly

```bash
python << 'EOF'
import sqlite3
conn = sqlite3.connect('continuum_knowledge.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM historical_periods WHERE location="Rome"')
print(f"Rome periods: {c.fetchone()[0]}")
conn.close()
EOF
```

Should output: `Rome periods: 5`

### Check 3: Test endpoint manually

```bash
# Start Flask in background
python app.py &
sleep 2

# Test Rome at 100 BC
curl -X POST http://localhost:5000/explore \
  -H "Content-Type: application/json" \
  -d '{"lat": 41.9, "lng": 12.5, "year": -100}' | python -m json.tool

# Should see knowledge_base_hit: true in response
```

## Next Steps to See More Results

### Add More Cities

To see results for Delhi, Athens, etc., run:

```bash
# When Wikipedia API is accessible, build knowledge base
python scripts/build_knowledge_base.py
```

Or create sample data for other cities similar to Rome.

### Expand Rome Coverage

To cover years outside -753 to 1650, add more periods to the database:
- Modern Rome (1650-2024)
- Pre-kingdom Rome (before -753)

---

## Summary

**Working:**
- ✅ Backend correctly returns period-specific data for Rome
- ✅ Knowledge base has 5 periods covering -753 to 1650
- ✅ Debug panel shows data source and period info
- ✅ Logarithmic time slider implemented
- ✅ Year zero handled correctly (1 BC → 1 AD)

**Not Yet Working:**
- ❌ Delhi, Athens, Baghdad (no knowledge base data)
- ❌ Rome for years outside -753 to 1650
- ❌ Wikipedia API fallback (blocked in this environment)

**Action Required:**
- Hard refresh browser (Ctrl+Shift+R)
- Restart Flask app
- Test Rome with slider positions 30-60% (covers -100 to 1500)
- Check debug panel to verify knowledge_base is being used
