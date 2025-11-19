#!/usr/bin/env python3
"""
Populate knowledge base with historical data for all cities

This script creates period-specific historical information for:
Rome, Athens, Cairo, Baghdad, Beijing, London, Paris, Delhi,
Istanbul, Venice, Kyiv, Jerusalem, Xi'an, Mexico City, Cuzco
"""

import sqlite3
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def init_knowledge_db():
    """Initialize knowledge base database with schema"""
    conn = sqlite3.connect('continuum_knowledge.db')
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

    conn.commit()
    conn.close()
    print("✓ Initialized knowledge base schema")


def populate_city_data(city_name, periods):
    """Generic function to populate data for any city"""
    conn = sqlite3.connect('continuum_knowledge.db')
    c = conn.cursor()

    inserted_count = 0
    for period in periods:
        try:
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

            inserted_count += 1
        except Exception as e:
            print(f"  Warning: Could not insert {period['period_name']}: {e}")

    conn.commit()
    conn.close()

    return inserted_count


# CITY DATA DEFINITIONS

ROME_PERIODS = [
    {
        'location': 'Rome',
        'period_name': 'Roman Kingdom',
        'start_year': -753,
        'end_year': -509,
        'description': 'The Roman Kingdom was the earliest period of Roman history when the city and its territory were ruled by kings. According to legend, Rome was founded by Romulus in 753 BC.',
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
        'description': 'The Roman Republic was established in 509 BC after the overthrow of the last king. It was characterized by a complex system of checks and balances.',
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
        'description': 'The Roman Empire began with Augustus becoming the first emperor in 27 BC. At its height, the empire controlled territories around the Mediterranean Sea.',
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
        'description': 'After the fall of the Western Roman Empire, Rome became the center of the Catholic Church and seat of the Papacy.',
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
        'description': 'Rome became a major center of the Renaissance, with Popes patronizing artists like Michelangelo and Raphael.',
        'source_page': 'Timeline of Rome',
        'facts': {
            'politics': 'Powerful Papal States under Renaissance Popes. Political intrigue and patronage.',
            'culture': 'Peak of Renaissance art and architecture. Sistine Chapel, St. Peters Basilica. Artists: Michelangelo, Raphael, Bernini.',
            'religion': 'Counter-Reformation headquarters. Council of Trent. Jesuit order founded.',
        }
    },
]

ATHENS_PERIODS = [
    {
        'location': 'Athens',
        'period_name': 'Archaic Athens',
        'start_year': -800,
        'end_year': -508,
        'description': 'Early Athens developed from small settlements into a major polis. Reforms by Solon and Cleisthenes laid foundations for democracy.',
        'source_page': 'Timeline of Athens',
        'facts': {
            'politics': 'Rule by aristocrats, then tyrants. Solon\'s reforms (594 BC) introduced democratic elements. Cleisthenes established demokratia (508 BC).',
            'culture': 'Development of pottery, trade expansion. Homer\'s epics influential. Early philosophy emerging.',
            'religion': 'Worship of Athena as patron goddess. Construction of early temples on Acropolis. Mystery cults at Eleusis.',
        }
    },
    {
        'location': 'Athens',
        'period_name': 'Classical Athens',
        'start_year': -508,
        'end_year': -323,
        'description': 'Golden Age of Athens under Pericles. Democracy flourished, philosophy and arts reached their peak.',
        'source_page': 'Timeline of Athens',
        'facts': {
            'politics': 'Direct democracy with Assembly (Ekklesia) and Council of 500. Pericles dominated politics. Led Delian League. Peloponnesian War with Sparta.',
            'culture': 'Parthenon built (447-432 BC). Socrates, Plato, Aristotle revolutionized philosophy. Tragedies by Sophocles, Euripides. Aristophanes\' comedies.',
            'religion': 'Panathenaic Festival honored Athena. Temple of Olympian Zeus. Oracle at Delphi consulted regularly.',
        }
    },
    {
        'location': 'Athens',
        'period_name': 'Hellenistic Athens',
        'start_year': -323,
        'end_year': -146,
        'description': 'After Alexander the Great, Athens lost political power but remained cultural and intellectual center.',
        'source_page': 'Timeline of Athens',
        'facts': {
            'politics': 'Under Macedonian influence. Garrison at Piraeus. Brief independence movements. Eventually fell to Rome in 146 BC.',
            'culture': 'Academy and Lyceum continued as major philosophical schools. Epicureanism and Stoicism founded. Library and Mouseion attracted scholars.',
            'religion': 'Traditional gods still worshipped. Mystery religions gained popularity. Influence of Eastern cults.',
        }
    },
    {
        'location': 'Athens',
        'period_name': 'Roman Athens',
        'start_year': -146,
        'end_year': 529,
        'description': 'Athens under Roman rule maintained status as university city and cultural destination.',
        'source_page': 'Timeline of Athens',
        'facts': {
            'politics': 'Part of Roman province of Achaea. Given some autonomy due to cultural prestige. Hadrian was major benefactor.',
            'culture': 'Remained premier center of learning. Romans sent sons to study philosophy. Hadrian\'s Library and Arch built. Theatre of Herodes Atticus.',
            'religion': 'Traditional polytheism coexisted with Christianity. Philosophical schools debate Christian doctrine. Closed by Justinian in 529 AD.',
        }
    },
]

CAIRO_PERIODS = [
    {
        'location': 'Cairo',
        'period_name': 'Ancient Memphis',
        'start_year': -3100,
        'end_year': -30,
        'description': 'Memphis (near modern Cairo) served as capital of ancient Egypt for over 3000 years.',
        'source_page': 'History of Cairo',
        'facts': {
            'politics': 'Capital of unified Egypt under pharaohs. Administrative center throughout Old, Middle, and New Kingdoms. Strategic location controlling Nile Delta.',
            'culture': 'Center of craftsmen and artists. Major cult center. Giza Pyramids built nearby. Scribal schools and libraries.',
            'religion': 'Temple of Ptah (creator god) was major religious site. Memphis triad: Ptah, Sekhmet, and Nefertem. Royal burials at nearby necropolises.',
        }
    },
    {
        'location': 'Cairo',
        'period_name': 'Fatimid Cairo',
        'start_year': 969,
        'end_year': 1171,
        'description': 'Cairo was founded in 969 AD by the Fatimid Caliphate as their capital city, Al-Qahira.',
        'source_page': 'History of Cairo',
        'facts': {
            'politics': 'Capital of Fatimid Caliphate. Shi\'a dynasty ruling North Africa and much of Middle East. Palace complexes and administrative buildings.',
            'culture': 'Al-Azhar Mosque founded (970 AD) - became premier center of Islamic learning. Flourishing arts, literature, and science. Tolerance of diverse communities.',
            'religion': 'Ismaili Shi\'a Islam as state religion. Al-Azhar taught Shi\'a theology. Coexistence of Sunni, Christian, and Jewish populations.',
        }
    },
    {
        'location': 'Cairo',
        'period_name': 'Mamluk Cairo',
        'start_year': 1250,
        'end_year': 1517,
        'description': 'Under Mamluk rule, Cairo became the greatest city in the Islamic world and major center of trade and learning.',
        'source_page': 'History of Cairo',
        'facts': {
            'politics': 'Capital of Mamluk Sultanate. Military slave dynasty ruling Egypt and Syria. Defeated Mongols and Crusaders. Complex system of military patronage.',
            'culture': 'Golden age of Islamic architecture: mosques, madrasas, mausoleums. Khan el-Khalili bazaar established. Center of Arabic literature and historiography.',
            'religion': 'Sunni Islam dominant. Al-Azhar shifted to Sunni teachings. Sufi orders prominent. Cairo held Islamic relics including Prophet\'s mantle.',
        }
    },
    {
        'location': 'Cairo',
        'period_name': 'Ottoman Cairo',
        'start_year': 1517,
        'end_year': 1867,
        'description': 'Cairo became provincial capital of Ottoman Empire while maintaining cultural and economic importance.',
        'source_page': 'History of Cairo',
        'facts': {
            'politics': 'Governed by Ottoman viceroy (Pasha). Mamluks retained local power as beys. Napoleon briefly occupied (1798-1801). Muhammad Ali dynasty began modernization.',
            'culture': 'Turkish influences mixed with Arabic traditions. Coffee houses as social centers. French Expedition brought scientific study and Description de l\'Égypte.',
            'religion': 'Sunni Ottoman orthodoxy. Al-Azhar remained independent intellectual center. Sufi tariqas widespread. Religious minorities organized in millets.',
        }
    },
]

BAGHDAD_PERIODS = [
    {
        'location': 'Baghdad',
        'period_name': 'Abbasid Golden Age',
        'start_year': 762,
        'end_year': 1055,
        'description': 'Baghdad was founded in 762 AD as the capital of the Abbasid Caliphate, becoming the world\'s largest and most prosperous city.',
        'source_page': 'History of Baghdad',
        'facts': {
            'politics': 'Capital of Abbasid Caliphate. Caliph held religious and political authority. Round City design by al-Mansur. Bureaucratic administration with viziers.',
            'culture': 'House of Wisdom (Bayt al-Hikma) - major center of translation and scholarship. Islamic Golden Age: astronomy, mathematics, medicine, philosophy. Al-Khwarizmi, Al-Kindi, and many others worked here.',
            'religion': 'Sunni caliphate. Center of Islamic learning and jurisprudence. Four major Sunni schools developed. Shi\'a and other minorities present.',
        }
    },
    {
        'location': 'Baghdad',
        'period_name': 'Seljuk and Late Abbasid',
        'start_year': 1055,
        'end_year': 1258,
        'description': 'Abbasid caliphs became figureheads under Seljuk Turkish sultans, who held real military and political power.',
        'source_page': 'History of Baghdad',
        'facts': {
            'politics': 'Seljuk sultans ruled as military protectors of caliphs. Caliphs retained religious legitimacy. Frequent conflicts with various Turkish dynasties.',
            'culture': 'Continued as center of learning despite political turmoil. Nizamiyya madrasas established. Persian literature flourished. Ibn Sina (Avicenna) and Al-Ghazali influenced philosophy.',
            'religion': 'Sunni orthodoxy emphasized. Sufism gained influence. Religious debates between different schools of thought. Tension with Fatimid Shi\'a caliphate.',
        }
    },
    {
        'location': 'Baghdad',
        'period_name': 'Ilkhanate Period',
        'start_year': 1258,
        'end_year': 1411,
        'description': 'After Mongol conquest destroyed the Abbasid caliphate, Baghdad declined but gradually recovered under Ilkhanate rule.',
        'source_page': 'History of Baghdad',
        'facts': {
            'politics': 'Mongol conquest (1258) devastated city. Ruled by Ilkhanate dynasty. Initially pagan, later converted to Islam. Shrank from over 1 million to ~100,000 inhabitants.',
            'culture': 'Libraries and House of Wisdom destroyed. Gradual cultural recovery. Persian and Mongol influences. Some scholars fled to other cities.',
            'religion': 'Abbasid caliphate ended. Ilkhanids converted to Islam (1295). Mixed Buddhist, Christian, and Islamic practices initially. Later Sunni Islam restored.',
        }
    },
    {
        'location': 'Baghdad',
        'period_name': 'Ottoman Baghdad',
        'start_year': 1534,
        'end_year': 1917,
        'description': 'Baghdad became Ottoman provincial capital, contested with Safavid Persia, gradually modernizing in 19th century.',
        'source_page': 'History of Baghdad',
        'facts': {
            'politics': 'Ottoman province (eyalet/vilayet). Governed by wali (governor). Constant border conflicts with Safavid/Qajar Persia. Contested between Sunni Ottoman and Shi\'a Persian empires.',
            'culture': 'Ottoman Turkish cultural influences. Traditional Arabic scholarship continued. 19th century Tanzimat reforms brought modernization. Printing press, schools, telegraph.',
            'religion': 'Sunni Ottoman rule over mixed Sunni-Shi\'a population. Shi\'a shrine cities (Najaf, Karbala) nearby. Religious tensions sometimes exploited politically.',
        }
    },
]

BEIJING_PERIODS = [
    {
        'location': 'Beijing',
        'period_name': 'Ancient Ji',
        'start_year': -1045,
        'end_year': 221,
        'description': 'Beijing area (as Ji/Yan) was capital of Yan state during Zhou dynasty, later conquered by Qin.',
        'source_page': 'History of Beijing',
        'facts': {
            'politics': 'Capital of Yan state during Zhou dynasty. Defended northern frontier. Warring States period saw conflicts. Qin conquest unified China (221 BC).',
            'culture': 'Northern frontier culture mixing Chinese and nomadic elements. Bronze casting, jade carving. Yan culture distinct from central plains.',
            'religion': 'Traditional Chinese ancestor worship and nature gods. Confucian values emerging late in period. Shamanistic practices from northern tribes.',
        }
    },
    {
        'location': 'Beijing',
        'period_name': 'Yuan Dynasty',
        'start_year': 1271,
        'end_year': 1368,
        'description': 'Kublai Khan established Yuan dynasty and made Dadu (Beijing) his capital, first time Beijing became China\'s capital.',
        'source_page': 'History of Beijing',
        'facts': {
            'politics': 'Capital of Mongol-ruled Yuan dynasty. Kublai Khan built grand capital Dadu. Multi-ethnic empire from Korea to Persia. Four-class system with Mongols at top.',
            'culture': 'Meeting point of East Asian, Central Asian, and Islamic cultures. Marco Polo visited. Grand Canal extended. Drama and vernacular novels flourished.',
            'religion': 'Religious tolerance: Buddhism, Islam, Christianity, Taoism coexisted. Tibetan Buddhism favored by court. Confucian civil service examination suspended.',
        }
    },
    {
        'location': 'Beijing',
        'period_name': 'Ming Dynasty',
        'start_year': 1368,
        'end_year': 1644,
        'description': 'The Yongle Emperor moved Ming capital to Beijing, building the Forbidden City and establishing Beijing as China\'s imperial center.',
        'source_page': 'History of Beijing',
        'facts': {
            'politics': 'Capital moved from Nanjing to Beijing (1421). Forbidden City built as imperial palace. Emperors ruled through bureaucracy of scholar-officials. Eunuchs gained significant power in later period.',
            'culture': 'Golden age of Chinese arts. Great Wall rebuilt/extended. Porcelain manufacture perfected. Vernacular novels: Journey to the West. Traditional opera developed.',
            'religion': 'Neo-Confucianism as state ideology. Buddhism and Taoism tolerated. Temple of Heaven built for imperial sacrifices. Matteo Ricci introduced Catholicism.',
        }
    },
    {
        'location': 'Beijing',
        'period_name': 'Qing Dynasty',
        'start_year': 1644,
        'end_year': 1912,
        'description': 'Manchu Qing dynasty ruled from Beijing, expanding empire to greatest extent. Ended with Xinhai Revolution.',
        'source_page': 'History of Beijing',
        'facts': {
            'politics': 'Manchu conquest dynasty. Maintained Forbidden City. Banner system of Manchu, Mongol, and Chinese forces. Zenith under Kangxi and Qianlong emperors. Decline after Opium Wars. Boxer Rebellion (1900).',
            'culture': 'Manchu-Chinese cultural synthesis. Qianlong emperor assembled vast art collections. Summer Palace and gardens built. Late period saw Western influences and reform attempts.',
            'religion': 'Manchu shamanism coexisted with Chinese religions. Tibetan Buddhism remained important. Jesuits served as court astronomers and artists. Late Qing saw Christian missionary activity.',
        }
    },
]

LONDON_PERIODS = [
    {
        'location': 'London',
        'period_name': 'Roman Londinium',
        'start_year': 43,
        'end_year': 410,
        'description': 'Romans founded Londinium around 43 AD, making it capital of Britannia province and major trading center.',
        'source_page': 'History of London',
        'facts': {
            'politics': 'Capital of Roman Britain. Governor\'s residence and military headquarters. Rebuilt after Boudica\'s revolt (60 AD). Major port and administrative center.',
            'culture': 'Roman infrastructure: roads, bridge, amphitheater, forum, basilica. Bath houses and temples. Latin language and Roman customs. Mosaic art and pottery.',
            'religion': 'Roman pantheon: Jupiter, Mars, Minerva temples. Mithraism popular among soldiers. Early Christianity present. Celtic gods syncretized with Roman deities.',
        }
    },
    {
        'location': 'London',
        'period_name': 'Medieval London',
        'start_year': 886,
        'end_year': 1485,
        'description': 'London reestablished by Alfred the Great, growing into England\'s largest city and commercial center.',
        'source_page': 'History of London',
        'facts': {
            'politics': 'Capital of England after Norman Conquest (1066). Tower of London built. Westminster Palace as royal residence. Lord Mayor and City of London corporation. Parliament developed.',
            'culture': 'Westminster Abbey and St. Paul\'s Cathedral built. Geoffrey Chaucer wrote Canterbury Tales. London Bridge with houses. Guilds controlled trades. Markets and fairs.',
            'religion': 'Catholic Church dominant. Westminster Abbey crowned kings. Religious orders: Franciscans, Dominicans. Pilgrimages to shrines. Wycliffe\'s Lollard movement.',
        }
    },
    {
        'location': 'London',
        'period_name': 'Tudor London',
        'start_year': 1485,
        'end_year': 1603,
        'description': 'London flourished under Tudor monarchs, experiencing Renaissance culture and Protestant Reformation.',
        'source_page': 'History of London',
        'facts': {
            'politics': 'Political center under Henry VII, Henry VIII, and Elizabeth I. Dissolution of monasteries. Royal palaces: Whitehall, Hampton Court. Growing mercantile power.',
            'culture': 'Renaissance flowering: Shakespeare, Marlowe, Globe Theatre. Printing spread literacy. Royal Exchange founded (1571). Grammar schools established.',
            'religion': 'English Reformation: break with Rome. Church of England established. Catholic-Protestant tensions. Religious persecution both ways. Protestant settlement under Elizabeth.',
        }
    },
    {
        'location': 'London',
        'period_name': 'Stuart London',
        'start_year': 1603,
        'end_year': 1714,
        'description': 'London survived plague, Great Fire, and Civil War to become Europe\'s largest city and financial capital.',
        'source_page': 'History of London',
        'facts': {
            'politics': 'Civil War: Royalists vs Parliamentarians. Charles I executed (1649). Restoration (1660). Glorious Revolution (1688). Parliament\'s power increased. Bank of England founded (1694).',
            'culture': 'Great Fire (1666) destroyed medieval city. Christopher Wren rebuilt St. Paul\'s. Coffee houses as intellectual centers. Royal Society founded. Samuel Pepys\' diary. Baroque architecture.',
            'religion': 'Anglican Church dominant. Puritans influential in Civil War. Religious tolerance increased post-1688. Catholic disabilities. Quakers and Dissenters persecuted.',
        }
    },
]

PARIS_PERIODS = [
    {
        'location': 'Paris',
        'period_name': 'Roman Lutetia',
        'start_year': -52,
        'end_year': 486,
        'description': 'Roman conquest transformed Gallic settlement of Lutetia into prosperous Roman town on left bank of Seine.',
        'source_page': 'History of Paris',
        'facts': {
            'politics': 'Part of Roman Gaul province. Administrative center for surrounding region. Julian proclaimed emperor here (360 AD). Defensive walls built against Germanic invasions.',
            'culture': 'Roman amphitheater, baths (Cluny), forum. Latin replaced Gaulish language. Roman villa culture. Roads connected to empire network.',
            'religion': 'Roman gods worshiped: Jupiter, Mercury, Mars. Christianity arrived 3rd century. St. Denis martyred (250s). Early Christian community grew.',
        }
    },
    {
        'location': 'Paris',
        'period_name': 'Medieval Paris',
        'start_year': 987,
        'end_year': 1453,
        'description': 'Paris became capital of Capetian France, growing into major European center of learning, religion, and commerce.',
        'source_page': 'History of Paris',
        'facts': {
            'politics': 'Capital of Kingdom of France. Royal palace on Île de la Cité. Louvre built as fortress (1190s). Estates-General meetings. Hundred Years War: English occupation (1420-36).',
            'culture': 'University of Paris (Sorbonne) founded ~1150 - premier European university. Gothic architecture: Notre-Dame Cathedral. Illuminated manuscripts. Courtly love literature.',
            'religion': 'Notre-Dame Cathedral (1163-1345). Center of Catholic theology. Peter Abelard, Thomas Aquinas taught. Sainte-Chapelle built for holy relics. Many monasteries and churches.',
        }
    },
    {
        'location': 'Paris',
        'period_name': 'Renaissance Paris',
        'start_year': 1453,
        'end_year': 1643,
        'description': 'Paris flourished under Renaissance kings, becoming Europe\'s largest city despite religious wars.',
        'source_page': 'History of Paris',
        'facts': {
            'politics': 'Capital of increasingly centralized monarchy. Francis I, Henry II brought Italian Renaissance culture. St. Bartholomew\'s Day Massacre (1572). Henry IV rebuilt and expanded city. Louvre expanded as royal palace.',
            'culture': 'French Renaissance architecture. Pont Neuf built. Tuileries Palace and gardens. French literature developed: Rabelais, Montaigne, Ronsard. Royal printing press.',
            'religion': 'Wars of Religion: Catholic vs Huguenot (Protestant). Catholic League strong. Henry IV converted: "Paris is worth a mass." Edict of Nantes (1598) granted tolerance.',
        }
    },
    {
        'location': 'Paris',
        'period_name': 'Ancien Régime Paris',
        'start_year': 1643,
        'end_year': 1789,
        'description': 'Paris under Louis XIV and XV became cultural capital of Europe, center of Enlightenment thought.',
        'source_page': 'History of Paris',
        'facts': {
            'politics': 'Absolute monarchy. Louis XIV moved court to Versailles but Paris remained administrative capital. Royal academies. Growing tension between monarchy and parlements. Pre-revolutionary ferment.',
            'culture': 'Enlightenment center: Voltaire, Rousseau, Diderot\'s Encyclopedia. Salons and cafés. Baroque and Rococo art. Place des Vosges, Les Invalides. Opera and theater flourished.',
            'religion': 'Catholic Church dominant. Jansenist controversy. Jesuits expelled (1764). Gallicanism asserted French church independence. Growing secularism among intellectuals.',
        }
    },
]

DELHI_PERIODS = [
    {
        'location': 'Delhi',
        'period_name': 'Delhi Sultanate',
        'start_year': 1206,
        'end_year': 1526,
        'description': 'Five successive dynasties ruled from Delhi, establishing first major Islamic kingdom in India.',
        'source_page': 'History of Delhi',
        'facts': {
            'politics': 'Capital of Muslim sultanate. Slave, Khalji, Tughlaq, Sayyid, and Lodi dynasties. Defeated Mongol invasions. Peak under Alauddin Khalji who controlled most of India.',
            'culture': 'Indo-Islamic architecture began: Qutb Minar, Tughlaqabad Fort. Persian language at court. Synthesis of Islamic and Indian traditions. Amir Khusro\'s poetry and music.',
            'religion': 'Sunni Islam as state religion. Sufi saints highly influential: Nizamuddin Auliya. Hindu majority population. Temple destruction but also some tolerance. Bhakti movement arose.',
        }
    },
    {
        'location': 'Delhi',
        'period_name': 'Mughal Delhi',
        'start_year': 1526,
        'end_year': 1857,
        'description': 'Delhi reached its zenith under Mughal emperors, becoming center of Indo-Persian culture and one of world\'s largest cities.',
        'source_page': 'History of Delhi',
        'facts': {
            'politics': 'Capital under several Mughals, especially Shah Jahan who built Shahjahanabad (Old Delhi). Red Fort as imperial palace. Efficient administration. Decline after Aurangzeb. Nadir Shah sacked city (1739). Marathas and British influence grew.',
            'culture': 'Peak of Mughal architecture: Red Fort, Jama Masjid, Humayun\'s Tomb. Miniature painting. Urdu language developed. Persian literature. Classical Hindustani music. Chandni Chowk bazaar.',
            'religion': 'Religious syncretism under Akbar. Jama Masjid - major mosque. Sufi dargahs. Sikhism emerged. Aurangzeb more orthodox. Hindu-Muslim cultural exchange in arts and festivals.',
        }
    },
    {
        'location': 'Delhi',
        'period_name': 'British Raj Delhi',
        'start_year': 1857,
        'end_year': 1947,
        'description': 'After 1857 uprising, British made Delhi their capital, building New Delhi as imperial capital.',
        'source_page': 'History of Delhi',
        'facts': {
            'politics': 'Capital shifted from Calcutta to Delhi (1911). New Delhi designed by Lutyens. Viceroy\'s House (Rashtrapati Bhavan). Center of Indian independence movement. Rowlatt Act protests, Quit India Movement.',
            'culture': 'New Delhi: wide avenues, government buildings blend European and Mughal styles. India Gate war memorial. Universities established. Newspapers and political discourse. Gandhi\'s ashram.',
            'religion': 'British respected but also exploited religious divisions. Hindu-Muslim tensions increased. Communal riots. Partition (1947) saw massive violence and displacement.',
        }
    },
]

ISTANBUL_PERIODS = [
    {
        'location': 'Istanbul',
        'period_name': 'Byzantine Constantinople',
        'start_year': 330,
        'end_year': 1204,
        'description': 'Constantine founded Constantinople as "New Rome", becoming capital of Byzantine Empire for over 1000 years.',
        'source_page': 'History of Istanbul',
        'facts': {
            'politics': 'Capital of Eastern Roman (Byzantine) Empire. Emperor held supreme authority. Hippodrome for chariot races and political expression. Survived multiple sieges. Peak under Justinian I.',
            'culture': 'Hagia Sophia built (537). Greek replaced Latin. Roman law codified (Justinian Code). Preserved classical learning. Mosaics and icons. Greek fire military technology.',
            'religion': 'Center of Eastern Orthodox Christianity. Patriarch of Constantinople. Iconoclasm controversy (8th-9th c.). Great Schism with Rome (1054). Monastery culture strong.',
        }
    },
    {
        'location': 'Istanbul',
        'period_name': 'Latin Constantinople',
        'start_year': 1204,
        'end_year': 1261,
        'description': 'Fourth Crusade conquered Constantinople, establishing short-lived Latin Empire.',
        'source_page': 'History of Istanbul',
        'facts': {
            'politics': 'Latin Empire ruled by Crusader nobles. Byzantine court fled to Nicaea. Venetians controlled key areas. Weak and divided rule. Recaptured by Byzantines in 1261.',
            'culture': 'Much destruction and looting during conquest. Many artworks taken to Venice. Latin replaced Greek in administration. Byzantine cultural traditions disrupted.',
            'religion': 'Catholic Latin Church imposed. Patriarch fled. Orthodox churches converted. Religious tensions high. Some forced conversions.',
        }
    },
    {
        'location': 'Istanbul',
        'period_name': 'Late Byzantine Constantinople',
        'start_year': 1261,
        'end_year': 1453,
        'description': 'Restored Byzantine Empire ruled from Constantinople, but city was shadow of former glory.',
        'source_page': 'History of Istanbul',
        'facts': {
            'politics': 'Palaiologos dynasty restored. Empire reduced to Constantinople and surroundings. Ottoman pressure increased. Civil wars. Attempts at church union with Rome for military aid failed.',
            'culture': 'Palaiologian Renaissance in art and literature. Scholars preserved Greek classics. Many intellectuals fled to Italy, helping spark Italian Renaissance.',
            'religion': 'Orthodox Christianity maintained. Theological debates with Catholics over Filioque and papal authority. Monasteries on Mt. Athos. Hesychasm mysticism.',
        }
    },
    {
        'location': 'Istanbul',
        'period_name': 'Ottoman Istanbul',
        'start_year': 1453,
        'end_year': 1922,
        'description': 'Mehmed II conquered Constantinople, making it capital of Ottoman Empire. Renamed Istanbul, it became Islamic imperial city.',
        'source_page': 'History of Istanbul',
        'facts': {
            'politics': 'Capital of Ottoman Empire. Topkapi Palace as sultan\'s residence. Center of vast empire spanning three continents. Tanzimat reforms modernized in 19th century. Revolution of 1908. Lost capital status to Ankara (1923).',
            'culture': 'Hagia Sophia converted to mosque. Ottoman classical architecture: Süleymaniye Mosque, Blue Mosque. Grand Bazaar. Turkish and Persian culture blend. Modernization in late period: universities, trams, telegraph.',
            'religion': 'Sunni Islam as state religion. Sultan also Caliph (from 1517). Millet system gave autonomy to religious communities: Greek Orthodox, Armenian, Jewish. Sufi orders influential. Some secularization late period.',
        }
    },
]

VENICE_PERIODS = [
    {
        'location': 'Venice',
        'period_name': 'Early Medieval Venice',
        'start_year': 697,
        'end_year': 1171,
        'description': 'Venice emerged as independent maritime city-state, building lagoon city and growing wealthy through trade with Byzantine Empire.',
        'source_page': 'History of Venice',
        'facts': {
            'politics': 'Republic with elected Doge as leader. Nominally Byzantine vassal but increasingly independent. Built unique lagoon city on wooden piles. Assembly of free men made decisions.',
            'culture': 'Unique architecture adapted to water: palaces on canals, bridges. St. Mark\'s Basilica built. Byzantine artistic influence. Shipbuilding expertise. Glass-making on Murano.',
            'religion': 'Catholic but maintained independence from Papal and Imperial politics. St. Mark adopted as patron saint (relics brought from Alexandria). Byzantine-style churches and mosaics.',
        }
    },
    {
        'location': 'Venice',
        'period_name': 'Maritime Republic',
        'start_year': 1171,
        'end_year': 1453,
        'description': 'Venice reached its peak as Mediterranean maritime power, dominating trade and establishing colonial empire.',
        'source_page': 'History of Venice',
        'facts': {
            'politics': 'Republic with Great Council, Senate, and Doge. Serrata (1297) restricted power to patrician families. Council of Ten handled security. Fourth Crusade (1204) gained territories. Rivalry with Genoa.',
            'culture': 'Gothic palaces line Grand Canal. Rialto Bridge. Carnival traditions developed. Marco Polo traveled to China. Arsenale (shipyard) employed thousands. Finest naval technology.',
            'religion': 'Catholic but fiercely independent from Pope. Venetian Patriarch. Religious brotherhoods (scuole) provided social services. Many churches built. Pragmatic about trade with Muslims.',
        }
    },
    {
        'location': 'Venice',
        'period_name': 'Renaissance Venice',
        'start_year': 1453,
        'end_year': 1630,
        'description': 'Though losing eastern territories to Ottomans, Venice flourished culturally as Renaissance art and music center.',
        'source_page': 'History of Venice',
        'facts': {
            'politics': 'Shifted focus to Italian mainland (Terra Firma). Wars with Ottoman Empire. Member of League of Cambrai conflicts. Sophisticated diplomacy. Declined relative to Atlantic powers but remained wealthy.',
            'culture': 'Venetian School of painting: Bellini, Giorgione, Titian, Tintoretto, Veronese. Palladio\'s architecture. Music: Gabrieli, Monteverdi. Printing center: Aldine Press. Commedia dell\'arte.',
            'religion': 'Catholic but resisted Inquisition and Papal authority. Interdict crisis with Pope Paul V. Jewish Ghetto established (1516) but community thrived. Religious tolerance for trade reasons.',
        }
    },
]

KYIV_PERIODS = [
    {
        'location': 'Kyiv',
        'period_name': 'Kievan Rus',
        'start_year': 882,
        'end_year': 1240,
        'description': 'Kyiv was capital of Kievan Rus, the first East Slavic state, serving as "Mother of Rus cities".',
        'source_page': 'History of Kyiv',
        'facts': {
            'politics': 'Capital of Kievan Rus federation. Grand Prince ruled from Kyiv. Peak under Yaroslav the Wise. Succession disputes weakened state. Trade center on Dnieper River.',
            'culture': 'Golden Gate entrance. St. Sophia Cathedral built (1037). Chronicles written. Cyrillic alphabet adopted. Yaroslav\'s law code. Architecture influenced by Byzantine style.',
            'religion': 'Conversion to Orthodox Christianity (988) under Vladimir. Byzantine rite adopted. Major churches built. Kyiv-Pechersk Lavra monastery founded (1051). Center of Orthodox Christianity for East Slavs.',
        }
    },
    {
        'location': 'Kyiv',
        'period_name': 'Polish-Lithuanian Kyiv',
        'start_year': 1362,
        'end_year': 1667,
        'description': 'After Mongol devastation, Kyiv came under Polish-Lithuanian control, experiencing Catholic influence and Cossack uprisings.',
        'source_page': 'History of Kyiv',
        'facts': {
            'politics': 'Part of Grand Duchy of Lithuania, then Polish-Lithuanian Commonwealth. Magdeburg rights granted (1494-97). Cossack Hetmanate uprisings. Khmelnitsky Uprising (1648). Ruin period of wars.',
            'culture': 'Kyiv-Mohyla Academy founded (1632) - major educational center. Ukrainian Baroque style. Cossack culture flourished. Printing introduced. Western European influences mixed with Orthodox traditions.',
            'religion': 'Orthodox Christianity maintained despite Catholic Polish rule. Union of Brest (1596) created Uniate Church. Religious tensions between Orthodox and Catholics. Petro Mohyla reformed Orthodox Church.',
        }
    },
    {
        'location': 'Kyiv',
        'period_name': 'Imperial Russian Kyiv',
        'start_year': 1667,
        'end_year': 1917,
        'description': 'Kyiv came under Russian control, becoming major city of Russian Empire and center of Ukrainian national revival.',
        'source_page': 'History of Kyiv',
        'facts': {
            'politics': 'Part of Russian Empire. Provincial capital. Russification policies. Growing Ukrainian national consciousness. 1905 Revolution unrest. Kiev was third largest city in Russian Empire by 1900.',
            'culture': 'Ukrainian literature and culture developed despite restrictions. Taras Shevchenko\'s poetry. St. Vladimir University founded (1834). Opera house, theaters. Industrialization in late 19th century.',
            'religion': 'Russian Orthodox Church dominant. Kyiv-Pechersk Lavra remained major pilgrimage site. St. Vladimir\'s Cathedral built (1862-96). Uniate Church suppressed. Some religious tolerance in late period.',
        }
    },
]

JERUSALEM_PERIODS = [
    {
        'location': 'Jerusalem',
        'period_name': 'Second Temple Period',
        'start_year': -516,
        'end_year': 70,
        'description': 'Jerusalem was center of Jewish life, rebuilt after Babylonian exile, reaching peak under Herodian dynasty.',
        'source_page': 'History of Jerusalem',
        'facts': {
            'politics': 'Under Persian, then Greek (Seleucid/Ptolemaic), then Roman rule. Hasmonean independence (140-63 BC). Herod the Great as client king rebuilt city. Roman province of Judea. First Jewish Revolt (66-73 AD).',
            'culture': 'Second Temple rebuilt (516 BC), expanded by Herod. Hebrew and Aramaic languages. Torah studied. Pharisees, Sadducees, Essenes. Dead Sea Scrolls. Jesus\' ministry.',
            'religion': 'Center of Jewish religious life. Temple worship, pilgrimage festivals. Synagogues developed. Sanhedrin council. Messianic expectations. Christianity emerged. Temple destroyed 70 AD.',
        }
    },
    {
        'location': 'Jerusalem',
        'period_name': 'Byzantine Jerusalem',
        'start_year': 324,
        'end_year': 638,
        'description': 'Jerusalem became holy Christian city, with churches built at sites of Jesus\' life, death, and resurrection.',
        'source_page': 'History of Jerusalem',
        'facts': {
            'politics': 'Part of Byzantine Empire. Constantine\'s mother Helena identified holy sites. Patriarchate of Jerusalem established. Persian conquest (614) briefly interrupted. Returned to Byzantine rule.',
            'culture': 'Church of the Holy Sepulchre built (335). Christian pilgrimage destination. Monasteries in Judean Desert. Mosaic art. Greek became dominant language.',
            'religion': 'Center of Christian pilgrimage. Church of the Holy Sepulchre, Mount of Olives churches. Patriarchate with theological debates. Jews banned from city. Samaritans persecuted.',
        }
    },
    {
        'location': 'Jerusalem',
        'period_name': 'Early Islamic Jerusalem',
        'start_year': 638,
        'end_year': 1099,
        'description': 'Muslim conquest made Jerusalem third holiest city in Islam. Dome of the Rock and Al-Aqsa Mosque built.',
        'source_page': 'History of Jerusalem',
        'facts': {
            'politics': 'Conquered by Caliph Umar (638). Under Umayyad, Abbasid, then Fatimid rule. Administrative center of Palestine. Relatively peaceful coexistence of religions.',
            'culture': 'Arabic became administrative language. Dome of the Rock built (691-692). Al-Aqsa Mosque. Islamic architecture and calligraphy. Scholars studied and taught.',
            'religion': 'Third holiest site in Islam after Mecca and Medina. Temple Mount (Haram al-Sharif) with Dome of the Rock. Christians allowed pilgrimage. Jews had limited access. Multi-religious city.',
        }
    },
    {
        'location': 'Jerusalem',
        'period_name': 'Crusader Kingdom',
        'start_year': 1099,
        'end_year': 1187,
        'description': 'Crusaders conquered Jerusalem, establishing Latin Kingdom until Saladin\'s reconquest.',
        'source_page': 'History of Jerusalem',
        'facts': {
            'politics': 'Capital of Latin Kingdom of Jerusalem. European feudal system. Frankish kings. Military orders: Knights Templar, Hospitaller. Palace at Temple Mount. Fell to Saladin (1187).',
            'culture': 'Romanesque churches built. European and Levantine cultures mixed. French as language of nobility. Castles and fortifications. Limited local Christian and Muslim population.',
            'religion': 'Catholic Latin Rite imposed. Patriarch appointed. Holy Sepulchre renovated. Dome of the Rock became church ("Templum Domini"). Jews and Muslims largely expelled. Pilgrimage center.',
        }
    },
    {
        'location': 'Jerusalem',
        'period_name': 'Mamluk and Ottoman Jerusalem',
        'start_year': 1260,
        'end_year': 1917,
        'description': 'Jerusalem under Muslim rule remained holy city for three faiths, with Ottoman reforms in 19th century.',
        'source_page': 'History of Jerusalem',
        'facts': {
            'politics': 'Mamluk rule (1260-1517), then Ottoman (1517-1917). Provincial capital. Suleiman rebuilt walls (1537-41). Tanzimat reforms. Growing European interest. British conquest (1917).',
            'culture': 'Islamic architecture: madrasas, ribats. Ottoman buildings. Printing came late. 19th century: European consulates, hospitals, schools. Multi-religious, multicultural character.',
            'religion': 'Muslim majority. Al-Aqsa and Dome of the Rock maintained. Christian pilgrimage continued. Jewish immigration increased, especially from 1800s. Western Wall became Jewish prayer site. Status quo agreement (1852) on holy sites.',
        }
    },
]

XIAN_PERIODS = [
    {
        'location': "Xi'an",
        'period_name': 'Qin Dynasty Chang\'an',
        'start_year': -221,
        'end_year': -206,
        'description': 'Qin Shi Huang, first Chinese emperor, established capital near Xi\'an, unifying China and standardizing script, currency, weights.',
        'source_page': 'History of Xi\'an',
        'facts': {
            'politics': 'First unified Chinese empire. Absolute centralized rule. Legalist philosophy implemented. Great Wall connected and expanded. Terracotta Army built for emperor\'s tomb.',
            'culture': 'Standardization of Chinese script, currency, and measurements. Book burning to enforce ideological conformity. Massive construction projects. Road network.',
            'religion': 'Legalist philosophy dominant, suppressing Confucianism. State cults. Emperor worship emerging. Shamanistic practices in tomb rituals.',
        }
    },
    {
        'location': "Xi'an",
        'period_name': 'Han Dynasty Chang\'an',
        'start_year': -206,
        'end_year': 220,
        'description': 'Chang\'an (Xi\'an) was capital of Western Han, becoming world\'s largest city and terminus of Silk Road.',
        'source_page': 'History of Xi\'an',
        'facts': {
            'politics': 'Capital of Western Han dynasty. Civil service examination system began. Expanded empire into Central Asia. Silk Road trade established. Peak under Emperor Wu.',
            'culture': 'Confucianism became state ideology. Historical records by Sima Qian. Silk production. Paper invented. Poetry flourished. Chang\'an had over 250,000 people.',
            'religion': 'Confucianism as official ideology. Taoism developed. Buddhism arrived from India via Silk Road. Ancestor worship. Imperial sacrifices to Heaven.',
        }
    },
    {
        'location': "Xi'an",
        'period_name': 'Tang Dynasty Chang\'an',
        'start_year': 618,
        'end_year': 907,
        'description': 'Chang\'an reached its zenith as world\'s largest and most cosmopolitan city, golden age of Chinese civilization.',
        'source_page': 'History of Xi\'an',
        'facts': {
            'politics': 'Capital of Tang dynasty - China\'s golden age. Population over 1 million in city, 2 million in metropolitan area. International city with foreign quarters. Peak of Chinese power and prosperity.',
            'culture': 'Golden age of Chinese poetry: Li Bai, Du Fu. Sophisticated city planning. Grand Palace. International trade hub. Persian, Arab, Central Asian merchants. Printing invented.',
            'religion': 'Buddhism at peak influence: Big Wild Goose Pagoda. Taoism patronized. Confucian bureaucracy. Nestorian Christianity, Zoroastrianism, Manichaeism, Islam all present. Religious tolerance.',
        }
    },
]

MEXICO_CITY_PERIODS = [
    {
        'location': 'Mexico City',
        'period_name': 'Aztec Tenochtitlan',
        'start_year': 1325,
        'end_year': 1521,
        'description': 'Mexica (Aztec) founded Tenochtitlan on island in Lake Texcoco, building magnificent city that became center of Triple Alliance empire.',
        'source_page': 'History of Mexico City',
        'facts': {
            'politics': 'Capital of Aztec Empire (Triple Alliance). Ruled by tlatoani (emperor). Tribute collected from conquered peoples. Peak under Moctezuma II. Population ~200,000-400,000.',
            'culture': 'Sophisticated city planning with causeways, canals, aqueducts. Templo Mayor (Great Temple). Chinampas (floating gardens) for agriculture. Pictographic writing. Advanced astronomy and mathematics. Vibrant markets.',
            'religion': 'Polytheistic. Huitzilopochtli (war/sun god) and Tlaloc (rain god) main deities. Human sacrifice central to religious practice. Elaborate rituals and festivals. Priestly class. Calendar systems.',
        }
    },
    {
        'location': 'Mexico City',
        'period_name': 'Spanish Colonial Mexico City',
        'start_year': 1521,
        'end_year': 1821,
        'description': 'Spanish conquered Tenochtitlan, building Mexico City on ruins as capital of New Spain.',
        'source_page': 'History of Mexico City',
        'facts': {
            'politics': 'Capital of Viceroyalty of New Spain. Spanish viceroy ruled. Encomienda and later hacienda systems. Creole resentment of Spanish-born officials grew. Independence movements began.',
            'culture': 'Spanish colonial Baroque architecture. Metropolitan Cathedral on Templo Mayor site. University founded (1551). Mixing of Spanish and indigenous cultures. Mestizo identity emerged. Sor Juana Inés de la Cruz.',
            'religion': 'Catholic Church dominant. Massive conversion effort. Monasteries and churches throughout city. Virgin of Guadalupe cult central to Mexican Catholicism. Inquisition active. Some indigenous beliefs syncretized.',
        }
    },
    {
        'location': 'Mexico City',
        'period_name': '19th Century Mexico City',
        'start_year': 1821,
        'end_year': 1910,
        'description': 'Mexico City remained capital through independence, reforms, and Porfirio Díaz\'s modernization.',
        'source_page': 'History of Mexico City',
        'facts': {
            'politics': 'Capital of independent Mexico. Political instability: multiple governments, civil wars. French intervention (1860s). Porfirio Díaz dictatorship (1876-1911) brought order and modernization.',
            'culture': 'Neoclassical and French-influenced architecture. Paseo de la Reforma created. Opera house, museums. Modernization under Díaz: electricity, trams, sewage. Growing inequality.',
            'religion': 'Catholic Church disestablished under Reform Laws (1850s-60s). Church property nationalized. Secular education. Religious tolerance legally granted. Church remained culturally important.',
        }
    },
]

CUZCO_PERIODS = [
    {
        'location': 'Cuzco',
        'period_name': 'Early Inca Cuzco',
        'start_year': 1200,
        'end_year': 1438,
        'description': 'Cuzco was local kingdom under early Inca rulers before imperial expansion.',
        'source_page': 'History of Cuzco',
        'facts': {
            'politics': 'Local kingdom among many Andean polities. Ruled by Inca (king) from Cuzco valley. Conflicts with neighboring groups. Limited territory.',
            'culture': 'Quechua language. Stone architecture developing. Oral traditions. Textile weaving. Terraced agriculture. Coca leaf cultivation.',
            'religion': 'Worship of Inti (sun god) and Pachamama (earth mother). Ancestor worship. Mountain deities (apus). Priestly class. Astronomical observations.',
        }
    },
    {
        'location': 'Cuzco',
        'period_name': 'Imperial Inca Cuzco',
        'start_year': 1438,
        'end_year': 1533,
        'description': 'Under Pachacuti and successors, Cuzco became capital of vast Inca Empire, rebuilt as magnificent imperial city.',
        'source_page': 'History of Cuzco',
        'facts': {
            'politics': 'Capital of Tawantinsuyu (Inca Empire) - largest pre-Columbian American empire. Divine emperor (Sapa Inca). Mit\'a labor system. Road network. Quipu record-keeping. Peak under Huayna Capac. Civil war between Atahualpa and Huáscar.',
            'culture': 'Cuzco rebuilt as planned city in puma shape. Sacsayhuamán fortress with massive fitted stones. Qorikancha (Temple of the Sun). No writing but sophisticated quipu. Machu Picchu built. Advanced stonework, metallurgy, textiles.',
            'religion': 'State religion centered on Inti (sun god). Sapa Inca considered divine. Qorikancha temple was empire\'s religious center. Human and animal sacrifices. Capacocha ritual. Ancestor mummy veneration.',
        }
    },
    {
        'location': 'Cuzco',
        'period_name': 'Spanish Colonial Cuzco',
        'start_year': 1533,
        'end_year': 1821,
        'description': 'Spanish conquest devastated Inca empire. Cuzco became Spanish colonial city while retaining indigenous population and some traditions.',
        'source_page': 'History of Cuzco',
        'facts': {
            'politics': 'Conquered by Francisco Pizarro (1533). Spanish colonial rule. Indigenous uprisings including Túpac Amaru II rebellion (1780-81). Encomienda system exploited indigenous labor. Mining economy.',
            'culture': 'Spanish built churches on Inca foundations. Colonial Baroque architecture. Cuzco School of painting. Spanish and Quechua languages coexisted. Mestizo culture developed. Many Inca walls preserved.',
            'religion': 'Forced Catholic conversion. Churches built on sacred Inca sites: Cathedral on Viracocha palace, churches on Qorikancha. Syncretic religious practices: Inti merged with Christian god. Corpus Christi festival incorporated indigenous elements.',
        }
    },
]


def main():
    """Populate knowledge base for all cities"""
    print("=" * 60)
    print("Continuum Knowledge Base - All Cities Population")
    print("=" * 60)

    # Initialize database
    init_knowledge_db()
    print()

    # List of all cities and their data
    all_cities = [
        ('Rome', ROME_PERIODS),
        ('Athens', ATHENS_PERIODS),
        ('Cairo', CAIRO_PERIODS),
        ('Baghdad', BAGHDAD_PERIODS),
        ('Beijing', BEIJING_PERIODS),
        ('London', LONDON_PERIODS),
        ('Paris', PARIS_PERIODS),
        ('Delhi', DELHI_PERIODS),
        ('Istanbul', ISTANBUL_PERIODS),
        ('Venice', VENICE_PERIODS),
        ('Kyiv', KYIV_PERIODS),
        ('Jerusalem', JERUSALEM_PERIODS),
        ("Xi'an", XIAN_PERIODS),
        ('Mexico City', MEXICO_CITY_PERIODS),
        ('Cuzco', CUZCO_PERIODS),
    ]

    total_periods = 0
    for city_name, periods in all_cities:
        print(f"Processing {city_name}...")
        count = populate_city_data(city_name, periods)
        print(f"  ✓ Added {count} periods")
        total_periods += count

    print()
    print("=" * 60)
    print(f"✓ Successfully populated knowledge base!")
    print(f"  Total cities: {len(all_cities)}")
    print(f"  Total periods: {total_periods}")
    print("=" * 60)


if __name__ == '__main__':
    main()
