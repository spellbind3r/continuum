#!/usr/bin/env python3
"""
Populate sample knowledge base data for testing

Since Wikipedia API may not always be accessible, this script
provides sample historical data for Rome to demonstrate the
knowledge base system.
"""

import sqlite3

def populate_rome_data():
    """Populate knowledge base with sample Rome historical data"""
    conn = sqlite3.connect('continuum_knowledge.db')
    c = conn.cursor()

    periods = [
        {
            'location': 'Rome',
            'period_name': 'Roman Kingdom',
            'start_year': -753,
            'end_year': -509,
            'description': 'The Roman Kingdom was the earliest period of Roman history when the city and its territory were ruled by kings. According to legend, Rome was founded by Romulus in 753 BC. During this period, Rome grew from a small settlement to a significant city-state.',
            'source_page': 'Timeline of Rome',
            'facts': {
                'politics': 'Ruled by a succession of seven kings, starting with Romulus. The king held supreme power and was advised by the Senate.',
                'culture': 'Early Roman culture was heavily influenced by neighboring Etruscans and Greeks. Latin language began to develop.',
                'religion': 'Polytheistic religion with gods like Jupiter, Mars, and Quirinus. Religious ceremonies were central to civic life.',
            }
        },
        {
            'location': 'Rome',
            'period_name': 'Roman Republic',
            'start_year': -509,
            'end_year': -27,
            'description': 'The Roman Republic was established in 509 BC after the overthrow of the last king. It was characterized by a complex system of checks and balances, with power shared between various assemblies, magistrates, and the Senate.',
            'source_page': 'Timeline of Rome',
            'facts': {
                'politics': 'Government by Senate and elected consuls. Major expansion through Italy and Mediterranean. Conflicts between patricians and plebeians.',
                'culture': 'Golden age of Latin literature with Cicero, Caesar, and Virgil. Development of Roman law and engineering.',
                'religion': 'Traditional Roman religion flourished. Major temples built to Jupiter, Juno, and Minerva.',
            }
        },
        {
            'location': 'Rome',
            'period_name': 'Roman Empire',
            'start_year': -27,
            'end_year': 476,
            'description': 'The Roman Empire began with Augustus becoming the first emperor in 27 BC. At its height, the empire controlled territories around the Mediterranean Sea and much of Europe, establishing Pax Romana.',
            'source_page': 'Timeline of Rome',
            'facts': {
                'politics': 'Imperial rule under emperors. Peak expansion under Trajan. Later period saw division into Eastern and Western empires.',
                'culture': 'Flourishing arts, architecture (Colosseum, Pantheon), and literature. Latin became lingua franca of the Mediterranean.',
                'religion': 'Traditional Roman religion initially, then gradual spread of Christianity. Constantine legalized Christianity in 313 AD.',
            }
        },
        {
            'location': 'Rome',
            'period_name': 'Medieval Rome',
            'start_year': 476,
            'end_year': 1420,
            'description': 'After the fall of the Western Roman Empire, Rome became the center of the Catholic Church. The city declined in population but gained spiritual authority as the seat of the Papacy.',
            'source_page': 'Timeline of Rome',
            'facts': {
                'politics': 'Papal control with conflicts between Popes and Holy Roman Emperors. Rome became capital of Papal States.',
                'culture': 'Preservation of classical texts in monasteries. Romanesque and Gothic architecture.',
                'religion': 'Center of Catholic Christianity. Construction of major basilicas. Pilgrimage destination.',
            }
        },
        {
            'location': 'Rome',
            'period_name': 'Renaissance Rome',
            'start_year': 1420,
            'end_year': 1650,
            'description': 'Rome became a major center of the Renaissance, with Popes patronizing artists like Michelangelo and Raphael. The city was rebuilt with magnificent churches, palaces, and public spaces.',
            'source_page': 'Timeline of Rome',
            'facts': {
                'politics': 'Powerful Papal States under Renaissance Popes. Political intrigue and patronage.',
                'culture': 'Peak of Renaissance art and architecture. Sistine Chapel, St. Peters Basilica. Artists: Michelangelo, Raphael, Bernini.',
                'religion': 'Counter-Reformation headquarters. Council of Trent. Jesuit order founded.',
            }
        },
    ]

    # Insert periods and facts
    for period in periods:
        c.execute('''
            INSERT OR REPLACE INTO historical_periods
            (location, period_name, start_year, end_year, description, source_page)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            period['location'],
            period['period_name'],
            period['start_year'],
            period['end_year'],
            period['description'],
            period['source_page']
        ))
        
        period_id = c.lastrowid
        
        # Insert facts for each category
        for category, content in period['facts'].items():
            c.execute('''
                INSERT INTO period_facts (period_id, category, content, confidence)
                VALUES (?, ?, ?, ?)
            ''', (period_id, category, content, 0.85))

    conn.commit()
    conn.close()

    print(f"✓ Successfully populated knowledge base with Rome historical data!")
    print(f"  Added {len(periods)} periods spanning 753 BC to 1650 AD")

if __name__ == '__main__':
    populate_rome_data()
