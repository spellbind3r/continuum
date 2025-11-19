# Knowledge Base Scripts

Scripts for building and populating the Continuum knowledge base.

## Scripts

### `build_knowledge_base.py`

Downloads and parses Wikipedia timeline pages into a structured local database.

**Usage:**
```bash
python scripts/build_knowledge_base.py
```

**What it does:**
- Downloads Wikipedia timeline pages (e.g., "Timeline of Rome")
- Parses historical periods with date ranges (e.g., "Roman Republic (509 BC – 27 BC)")
- Extracts descriptions and events
- Stores in `continuum_knowledge.db` with tables:
  - `historical_periods` - period name, start/end years, description
  - `period_facts` - category-specific information (politics, culture, religion)
  - `year_events` - year-specific events

**Current sources:**
- Rome: "Timeline of Rome"

**Note:** Requires internet access to Wikipedia API. If Wikipedia is blocked, use `populate_sample_data.py` instead.

---

### `populate_sample_data.py`

Populates the knowledge base with sample historical data for testing.

**Usage:**
```bash
python scripts/populate_sample_data.py
```

**What it does:**
- Creates sample historical data for Rome (753 BC - 1650 AD)
- Includes 5 periods: Roman Kingdom, Roman Republic, Roman Empire, Medieval Rome, Renaissance Rome
- Each period has Politics, Culture, and Religion categories
- Works offline without Wikipedia API access

**Use this when:**
- Wikipedia API is not accessible
- Testing the knowledge base system
- Demonstrating the hybrid lookup flow

---

## Database Schema

The knowledge base uses SQLite with the following structure:

```sql
-- Historical periods table
CREATE TABLE historical_periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    period_name TEXT NOT NULL,
    start_year INTEGER,
    end_year INTEGER,
    description TEXT,
    source_page TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(location, period_name)
);

-- Period facts by category
CREATE TABLE period_facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    confidence FLOAT DEFAULT 0.8,
    source_section TEXT,
    FOREIGN KEY (period_id) REFERENCES historical_periods(id)
);

-- Year-specific events
CREATE TABLE year_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    location TEXT NOT NULL,
    event TEXT NOT NULL,
    category TEXT,
    source_page TEXT
);
```

---

## Adding New Cities

To add knowledge for a new city:

1. **Edit `build_knowledge_base.py`:**
   ```python
   KNOWLEDGE_SOURCES = {
       'Rome': {
           'timeline': 'Timeline of Rome',
           'history': 'History of Rome',
       },
       'Athens': {  # Add new city
           'timeline': 'Timeline of Athens',
           'history': 'History of Athens',
       }
   }
   ```

2. **Run the builder:**
   ```bash
   python scripts/build_knowledge_base.py
   ```

3. **Verify in app:**
   - Start app: `python app.py`
   - Click on Athens
   - Check debug panel shows "knowledge_base" as source

---

## Troubleshooting

**"Access denied" or "403 Forbidden":**
- Wikipedia API may be rate-limited or blocked
- Use `populate_sample_data.py` for testing
- The app will fall back to real-time Wikipedia queries automatically

**"No data found for city X":**
- Check if the city is defined in `KNOWLEDGE_SOURCES`
- Verify Wikipedia has a timeline page for that city
- Check database: `SELECT * FROM historical_periods WHERE location = 'X'`

**"Knowledge base error":**
- Check database file exists: `ls -lh continuum_knowledge.db`
- Verify database schema: Run `build_knowledge_base.py` to recreate tables
