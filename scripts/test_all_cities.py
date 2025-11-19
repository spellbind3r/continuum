#!/usr/bin/env python3
"""
Automated tests for all cities in the knowledge base

Tests each city at multiple time periods to verify:
- Data exists for expected periods
- Categories are populated
- Content quality is reasonable
"""

import sqlite3
import sys

# Test cases: (city, year, expected_period_name)
TEST_CASES = [
    # Rome
    ('Rome', -600, 'Roman Kingdom'),
    ('Rome', -100, 'Roman Republic'),
    ('Rome', 200, 'Roman Empire'),
    ('Rome', 1000, 'Medieval Rome'),
    ('Rome', 1500, 'Renaissance Rome'),

    # Athens
    ('Athens', -700, 'Archaic Athens'),
    ('Athens', -400, 'Classical Athens'),
    ('Athens', -200, 'Hellenistic Athens'),
    ('Athens', 300, 'Roman Athens'),

    # Cairo
    ('Cairo', -2000, 'Ancient Memphis'),
    ('Cairo', 1000, 'Fatimid Cairo'),
    ('Cairo', 1300, 'Mamluk Cairo'),
    ('Cairo', 1700, 'Ottoman Cairo'),

    # Baghdad
    ('Baghdad', 800, 'Abbasid Golden Age'),
    ('Baghdad', 1100, 'Seljuk and Late Abbasid'),
    ('Baghdad', 1300, 'Ilkhanate Period'),
    ('Baghdad', 1700, 'Ottoman Baghdad'),

    # Beijing
    ('Beijing', -500, 'Ancient Ji'),
    ('Beijing', 1300, 'Yuan Dynasty'),
    ('Beijing', 1500, 'Ming Dynasty'),
    ('Beijing', 1800, 'Qing Dynasty'),

    # London
    ('London', 200, 'Roman Londinium'),
    ('London', 1200, 'Medieval London'),
    ('London', 1550, 'Tudor London'),
    ('London', 1650, 'Stuart London'),

    # Paris
    ('Paris', 100, 'Roman Lutetia'),
    ('Paris', 1200, 'Medieval Paris'),
    ('Paris', 1500, 'Renaissance Paris'),
    ('Paris', 1700, 'Ancien Régime Paris'),

    # Delhi
    ('Delhi', 1300, 'Delhi Sultanate'),
    ('Delhi', 1650, 'Mughal Delhi'),
    ('Delhi', 1900, 'British Raj Delhi'),

    # Istanbul
    ('Istanbul', 500, 'Byzantine Constantinople'),
    ('Istanbul', 1220, 'Latin Constantinople'),
    ('Istanbul', 1300, 'Late Byzantine Constantinople'),
    ('Istanbul', 1700, 'Ottoman Istanbul'),

    # Venice
    ('Venice', 900, 'Early Medieval Venice'),
    ('Venice', 1300, 'Maritime Republic'),
    ('Venice', 1500, 'Renaissance Venice'),

    # Kyiv
    ('Kyiv', 1000, 'Kievan Rus'),
    ('Kyiv', 1500, 'Polish-Lithuanian Kyiv'),
    ('Kyiv', 1800, 'Imperial Russian Kyiv'),

    # Jerusalem
    ('Jerusalem', -300, 'Second Temple Period'),
    ('Jerusalem', 500, 'Byzantine Jerusalem'),
    ('Jerusalem', 900, 'Early Islamic Jerusalem'),
    ('Jerusalem', 1150, 'Crusader Kingdom'),
    ('Jerusalem', 1500, 'Mamluk and Ottoman Jerusalem'),

    # Xi'an
    ("Xi'an", -215, "Qin Dynasty Chang'an"),  # Qin: -221 to -206
    ("Xi'an", 100, "Han Dynasty Chang'an"),
    ("Xi'an", 750, "Tang Dynasty Chang'an"),

    # Mexico City
    ('Mexico City', 1400, 'Aztec Tenochtitlan'),
    ('Mexico City', 1700, 'Spanish Colonial Mexico City'),
    ('Mexico City', 1850, '19th Century Mexico City'),

    # Cuzco
    ('Cuzco', 1300, 'Early Inca Cuzco'),
    ('Cuzco', 1500, 'Imperial Inca Cuzco'),
    ('Cuzco', 1700, 'Spanish Colonial Cuzco'),
]


def query_knowledge_base(conn, location, year):
    """Query the knowledge base for a city at a specific year"""
    c = conn.cursor()

    # Find the period this year falls into
    c.execute('''
        SELECT period_name, start_year, end_year, description
        FROM historical_periods
        WHERE location = ?
          AND start_year <= ?
          AND end_year >= ?
        LIMIT 1
    ''', (location, year, year))

    period = c.fetchone()

    if not period:
        return None

    period_name, start_year, end_year, description = period

    # Get facts for this period
    c.execute('''
        SELECT hp.id FROM historical_periods hp
        WHERE hp.location = ?
          AND hp.start_year <= ?
          AND hp.end_year >= ?
    ''', (location, year, year))

    period_id_result = c.fetchone()
    if not period_id_result:
        return None

    period_id = period_id_result[0]

    c.execute('''
        SELECT category, content, confidence
        FROM period_facts
        WHERE period_id = ?
    ''', (period_id,))

    facts = c.fetchall()

    return {
        'period_name': period_name,
        'start_year': start_year,
        'end_year': end_year,
        'description': description,
        'facts': facts
    }


def main():
    """Run all tests"""
    print("=" * 80)
    print("Continuum Knowledge Base - Automated Quality Tests")
    print("=" * 80)
    print()

    # Connect to database
    try:
        conn = sqlite3.connect('continuum_knowledge.db')
    except Exception as e:
        print(f"❌ FATAL: Could not connect to database: {e}")
        print("   Make sure you've run: python scripts/populate_all_cities.py")
        sys.exit(1)

    total_tests = len(TEST_CASES)
    passed = 0
    failed = 0
    issues = []

    # Run tests
    for city, year, expected_period in TEST_CASES:
        result = query_knowledge_base(conn, city, year)

        if result is None:
            failed += 1
            issues.append({
                'city': city,
                'year': year,
                'expected': expected_period,
                'issue': 'NO DATA FOUND',
                'severity': 'HIGH'
            })
            print(f"❌ {city:20s} {year:6d}: NO DATA (expected {expected_period})")

        elif result['period_name'] != expected_period:
            failed += 1
            issues.append({
                'city': city,
                'year': year,
                'expected': expected_period,
                'found': result['period_name'],
                'issue': 'WRONG PERIOD',
                'severity': 'MEDIUM'
            })
            print(f"⚠️  {city:20s} {year:6d}: {result['period_name']} (expected {expected_period})")

        else:
            # Check quality
            has_issues = False
            quality_issues = []

            # Check if we have at least 2 categories
            if len(result['facts']) < 2:
                quality_issues.append(f"only {len(result['facts'])} categories")
                has_issues = True

            # Check if content is too short
            for category, content, confidence in result['facts']:
                if len(content) < 50:
                    quality_issues.append(f"{category} too short ({len(content)} chars)")
                    has_issues = True

            if has_issues:
                issues.append({
                    'city': city,
                    'year': year,
                    'period': result['period_name'],
                    'issue': ', '.join(quality_issues),
                    'severity': 'LOW'
                })
                print(f"⚠️  {city:20s} {year:6d}: {result['period_name']} - {', '.join(quality_issues)}")
            else:
                passed += 1
                print(f"✓  {city:20s} {year:6d}: {result['period_name']}")

    conn.close()

    # Summary
    print()
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"Total tests: {total_tests}")
    print(f"✓ Passed: {passed} ({100*passed//total_tests}%)")
    print(f"❌ Failed: {failed} ({100*failed//total_tests}%)")

    if issues:
        print()
        print("Issues Found:")
        print("-" * 80)

        # Group by severity
        high_issues = [i for i in issues if i.get('severity') == 'HIGH']
        medium_issues = [i for i in issues if i.get('severity') == 'MEDIUM']
        low_issues = [i for i in issues if i.get('severity') == 'LOW']

        if high_issues:
            print(f"\n🔴 HIGH SEVERITY ({len(high_issues)}):")
            for issue in high_issues:
                print(f"   {issue['city']} at {issue['year']}: {issue['issue']}")
                print(f"   Expected: {issue['expected']}")

        if medium_issues:
            print(f"\n🟡 MEDIUM SEVERITY ({len(medium_issues)}):")
            for issue in medium_issues:
                print(f"   {issue['city']} at {issue['year']}: {issue['issue']}")
                print(f"   Expected: {issue['expected']}, Found: {issue['found']}")

        if low_issues:
            print(f"\n🟢 LOW SEVERITY ({len(low_issues)}):")
            for issue in low_issues:
                print(f"   {issue['city']} at {issue['year']} ({issue['period']}): {issue['issue']}")

    print()
    print("=" * 80)

    if passed == total_tests:
        print("✅ ALL TESTS PASSED!")
    elif failed == 0:
        print("✅ All critical tests passed (only minor quality issues)")
    else:
        print(f"⚠️  {failed} tests failed - review issues above")

    print("=" * 80)

    # Exit code
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
