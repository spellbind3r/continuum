#!/usr/bin/env python3
"""
Knowledge Base Builder for Continuum

This script downloads and parses Wikipedia timeline/history pages
into a structured local knowledge base.

Usage:
    python scripts/build_knowledge_base.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import wikipediaapi
import sqlite3
import re
import json
from datetime import datetime

# Knowledge base database
KB_DB_PATH = 'continuum_knowledge.db'

# Define timeline sources for cities
KNOWLEDGE_SOURCES = {
    'Rome': {
        'timeline': 'Timeline of Rome',
        'history': 'History of Rome',
        'periods': [
            'Roman Kingdom',
            'Roman Republic',
            'Roman Empire',
            'Byzantine Empire'
        ]
    }
    # Add more cities as we expand
}

def init_knowledge_db():
    """Initialize knowledge base database"""
    conn = sqlite3.connect(KB_DB_PATH)
    c = conn.cursor()

    # Historical periods table
    c.execute('''
        CREATE TABLE IF NOT EXISTS historical_periods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            period_name TEXT NOT NULL,
            start_year INTEGER,
            end_year INTEGER,
            description TEXT,
            source_page TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(location, period_name)
        )
    ''')

    # Period facts by category
    c.execute('''
        CREATE TABLE IF NOT EXISTS period_facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            period_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            confidence FLOAT DEFAULT 0.8,
            source_section TEXT,
            FOREIGN KEY (period_id) REFERENCES historical_periods(id)
        )
    ''')

    # Year-specific events
    c.execute('''
        CREATE TABLE IF NOT EXISTS year_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            location TEXT NOT NULL,
            event TEXT NOT NULL,
            category TEXT,
            source_page TEXT
        )
    ''')

    # Indexes for fast lookup
    c.execute('CREATE INDEX IF NOT EXISTS idx_period_lookup ON historical_periods(location, start_year, end_year)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_year_lookup ON year_events(location, year)')

    conn.commit()
    conn.close()
    print(f"✓ Initialized knowledge database: {KB_DB_PATH}")

def parse_date_range(date_str):
    """
    Parse date ranges like:
    - "753 BC – 509 BC"
    - "509 BC – 27 BC"
    - "27 BC – 476 AD"
    """
    # Remove various dash types and normalize
    date_str = re.sub(r'[–—−]', '-', date_str)

    # Pattern: number + BC/AD/BCE/CE
    pattern = r'(\d+)\s*(BC|AD|BCE|CE)?'
    matches = re.findall(pattern, date_str)

    if len(matches) < 2:
        return None, None

    start_year = int(matches[0][0])
    if matches[0][1] in ['BC', 'BCE']:
        start_year = -start_year

    end_year = int(matches[1][0])
    if matches[1][1] in ['BC', 'BCE']:
        end_year = -end_year

    return start_year, end_year

def download_and_parse_timeline(city, timeline_page_name):
    """Download and parse a timeline page from Wikipedia"""
    print(f"\nProcessing {city}...")
    print(f"  Downloading: {timeline_page_name}")

    wiki = wikipediaapi.Wikipedia('Continuum/1.0 (knowledge-builder)', 'en')
    page = wiki.page(timeline_page_name)

    if not page.exists():
        print(f"  ✗ Page not found: {timeline_page_name}")
        return None

    print(f"  ✓ Downloaded ({len(page.text)} chars)")

    # Parse the timeline
    periods = parse_timeline_structure(page.text, page.summary)

    print(f"  ✓ Extracted {len(periods)} periods")
    return periods

def parse_timeline_structure(page_text, page_summary):
    """
    Parse Wikipedia page into structured periods

    Looking for sections like:
    == Roman Kingdom (753 BC – 509 BC) ==
    == Roman Republic (509 BC – 27 BC) ==
    """
    periods = []

    # Find major sections with date ranges
    # Pattern: == Title (date range) ==
    section_pattern = r'==+\s*([^=]+?)\s*\(([^)]+)\)\s*==+'

    for match in re.finditer(section_pattern, page_text):
        period_name = match.group(1).strip()
        date_range = match.group(2).strip()

        start_year, end_year = parse_date_range(date_range)

        if start_year is None:
            continue

        # Extract content for this section (until next == header)
        section_start = match.end()
        next_section = re.search(r'\n==', page_text[section_start:])
        section_end = section_start + next_section.start() if next_section else len(page_text)

        section_content = page_text[section_start:section_end].strip()

        # Extract first paragraph as description
        paragraphs = [p.strip() for p in section_content.split('\n\n') if p.strip() and not p.strip().startswith('*')]
        description = paragraphs[0][:500] if paragraphs else ""

        periods.append({
            'name': period_name,
            'start_year': start_year,
            'end_year': end_year,
            'description': description,
            'content': section_content
        })

    return periods

def store_periods_in_db(city, periods, source_page):
    """Store parsed periods in knowledge database"""
    conn = sqlite3.connect(KB_DB_PATH)
    c = conn.cursor()

    for period in periods:
        # Insert period
        c.execute('''
            INSERT OR REPLACE INTO historical_periods
            (location, period_name, start_year, end_year, description, source_page)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            city,
            period['name'],
            period['start_year'],
            period['end_year'],
            period['description'],
            source_page
        ))

        period_id = c.lastrowid

        # Extract and store facts by category
        # For now, store the overview
        c.execute('''
            INSERT INTO period_facts (period_id, category, content, confidence)
            VALUES (?, ?, ?, ?)
        ''', (period_id, 'overview', period['description'], 0.85))

    conn.commit()
    conn.close()
    print(f"  ✓ Stored {len(periods)} periods in database")

def build_knowledge_for_city(city, sources):
    """Build knowledge base for a specific city"""
    timeline_page = sources.get('timeline')

    if not timeline_page:
        print(f"✗ No timeline page defined for {city}")
        return

    # Download and parse
    periods = download_and_parse_timeline(city, timeline_page)

    if periods:
        store_periods_in_db(city, periods, timeline_page)

    return periods

def main():
    """Main entry point"""
    print("=" * 60)
    print("Continuum Knowledge Base Builder")
    print("=" * 60)

    # Initialize database
    init_knowledge_db()

    # Build knowledge for each city
    total_periods = 0
    for city, sources in KNOWLEDGE_SOURCES.items():
        periods = build_knowledge_for_city(city, sources)
        if periods:
            total_periods += len(periods)

    print("\n" + "=" * 60)
    print(f"✓ Knowledge base build complete!")
    print(f"  Total periods: {total_periods}")
    print(f"  Database: {KB_DB_PATH}")
    print("=" * 60)

if __name__ == '__main__':
    main()
