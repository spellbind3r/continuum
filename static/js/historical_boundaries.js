/**
 * Historical Boundaries Data
 * GeoJSON polygon data for major kingdoms, empires, and regions across history
 *
 * Data structure: Array of objects with:
 * - start_year: Beginning year of this boundary
 * - end_year: End year of this boundary
 * - name: Name of kingdom/empire/region
 * - type: Type (Empire, Kingdom, City-State, Caliphate, etc.)
 * - layer_type: kingdoms, languages, religions (for future layer control)
 * - geometry: GeoJSON polygon coordinates [longitude, latitude]
 */

const HISTORICAL_BOUNDARIES = [
    // ====================================================================
    // ANCIENT ROME (-753 to 476 CE)
    // ====================================================================
    {
        start_year: -753,
        end_year: -509,
        name: 'Roman Kingdom',
        type: 'Kingdom',
        layer_type: 'kingdoms',
        capital: 'Rome',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [12.3, 41.7], [12.6, 41.7], [12.6, 42.0], [12.3, 42.0], [12.3, 41.7]
            ]]
        }
    },
    {
        start_year: -509,
        end_year: -27,
        name: 'Roman Republic',
        type: 'Republic',
        layer_type: 'kingdoms',
        capital: 'Rome',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                // Italy peninsula + expanding territories
                [6.5, 36.0], [20.0, 36.0], [20.0, 46.0], [6.5, 46.0], [6.5, 36.0]
            ]]
        }
    },
    {
        start_year: -27,
        end_year: 200,
        name: 'Roman Empire (Peak)',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Rome',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                // Mediterranean basin at peak
                [-9.0, 35.0], [40.0, 35.0], [40.0, 53.0], [15.0, 53.0],
                [10.0, 47.0], [-9.0, 43.0], [-9.0, 35.0]
            ]]
        }
    },
    {
        start_year: 200,
        end_year: 476,
        name: 'Western Roman Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Rome/Ravenna',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                // Western portion, declining
                [-9.0, 36.0], [20.0, 36.0], [20.0, 50.0], [-9.0, 50.0], [-9.0, 36.0]
            ]]
        }
    },
    {
        start_year: 330,
        end_year: 1453,
        name: 'Byzantine Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Constantinople',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                // Eastern Mediterranean
                [20.0, 32.0], [45.0, 32.0], [45.0, 45.0], [20.0, 45.0], [20.0, 32.0]
            ]]
        }
    },

    // ====================================================================
    // ANCIENT GREECE (-800 to -146 BCE)
    // ====================================================================
    {
        start_year: -800,
        end_year: -500,
        name: 'Archaic Greek City-States',
        type: 'City-States',
        layer_type: 'kingdoms',
        capital: 'Various',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [19.0, 35.0], [28.0, 35.0], [28.0, 42.0], [19.0, 42.0], [19.0, 35.0]
            ]]
        }
    },
    {
        start_year: -500,
        end_year: -323,
        name: 'Classical Greece',
        type: 'City-States',
        layer_type: 'kingdoms',
        capital: 'Athens/Sparta',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [19.0, 34.0], [29.0, 34.0], [29.0, 42.0], [19.0, 42.0], [19.0, 34.0]
            ]]
        }
    },
    {
        start_year: -336,
        end_year: -323,
        name: 'Macedonian Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Pella/Babylon',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                // Alexander's conquests
                [15.0, 25.0], [75.0, 25.0], [75.0, 45.0], [15.0, 45.0], [15.0, 25.0]
            ]]
        }
    },

    // ====================================================================
    // PERSIA (-550 to 651 CE)
    // ====================================================================
    {
        start_year: -550,
        end_year: -330,
        name: 'Achaemenid Persian Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Persepolis',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                // Massive empire from Egypt to India
                [25.0, 20.0], [75.0, 20.0], [75.0, 45.0], [25.0, 45.0], [25.0, 20.0]
            ]]
        }
    },
    {
        start_year: 224,
        end_year: 651,
        name: 'Sassanid Persian Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Ctesiphon',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [40.0, 25.0], [70.0, 25.0], [70.0, 42.0], [40.0, 42.0], [40.0, 25.0]
            ]]
        }
    },

    // ====================================================================
    // ANCIENT EGYPT (-3100 to -30 BCE)
    // ====================================================================
    {
        start_year: -3100,
        end_year: -2686,
        name: 'Early Dynastic Egypt',
        type: 'Kingdom',
        layer_type: 'kingdoms',
        capital: 'Memphis',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [29.0, 22.0], [35.0, 22.0], [35.0, 32.0], [29.0, 32.0], [29.0, 22.0]
            ]]
        }
    },
    {
        start_year: -2686,
        end_year: -2181,
        name: 'Old Kingdom Egypt',
        type: 'Kingdom',
        layer_type: 'kingdoms',
        capital: 'Memphis',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [29.0, 22.0], [35.0, 22.0], [35.0, 32.0], [29.0, 32.0], [29.0, 22.0]
            ]]
        }
    },
    {
        start_year: -1550,
        end_year: -1077,
        name: 'New Kingdom Egypt',
        type: 'Kingdom',
        layer_type: 'kingdoms',
        capital: 'Thebes',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                // Expanded empire
                [27.0, 20.0], [40.0, 20.0], [40.0, 32.0], [27.0, 32.0], [27.0, 20.0]
            ]]
        }
    },
    {
        start_year: -332,
        end_year: -30,
        name: 'Ptolemaic Egypt',
        type: 'Kingdom',
        layer_type: 'kingdoms',
        capital: 'Alexandria',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [25.0, 22.0], [37.0, 22.0], [37.0, 32.0], [25.0, 32.0], [25.0, 22.0]
            ]]
        }
    },

    // ====================================================================
    // CHINA (-221 to 1912 CE)
    // ====================================================================
    {
        start_year: -221,
        end_year: -206,
        name: 'Qin Dynasty',
        type: 'Dynasty',
        layer_type: 'kingdoms',
        capital: "Chang'an",
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [100.0, 25.0], [120.0, 25.0], [120.0, 42.0], [100.0, 42.0], [100.0, 25.0]
            ]]
        }
    },
    {
        start_year: -206,
        end_year: 220,
        name: 'Han Dynasty',
        type: 'Dynasty',
        layer_type: 'kingdoms',
        capital: "Chang'an/Luoyang",
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [95.0, 20.0], [125.0, 20.0], [125.0, 45.0], [95.0, 45.0], [95.0, 20.0]
            ]]
        }
    },
    {
        start_year: 618,
        end_year: 907,
        name: 'Tang Dynasty',
        type: 'Dynasty',
        layer_type: 'kingdoms',
        capital: "Chang'an",
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [90.0, 18.0], [130.0, 18.0], [130.0, 48.0], [90.0, 48.0], [90.0, 18.0]
            ]]
        }
    },
    {
        start_year: 1368,
        end_year: 1644,
        name: 'Ming Dynasty',
        type: 'Dynasty',
        layer_type: 'kingdoms',
        capital: 'Beijing',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [95.0, 18.0], [125.0, 18.0], [125.0, 45.0], [95.0, 45.0], [95.0, 18.0]
            ]]
        }
    },
    {
        start_year: 1644,
        end_year: 1912,
        name: 'Qing Dynasty',
        type: 'Dynasty',
        layer_type: 'kingdoms',
        capital: 'Beijing',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [75.0, 15.0], [135.0, 15.0], [135.0, 53.0], [75.0, 53.0], [75.0, 15.0]
            ]]
        }
    },

    // ====================================================================
    // ISLAMIC CALIPHATES (622 to 1924 CE)
    // ====================================================================
    {
        start_year: 622,
        end_year: 661,
        name: 'Rashidun Caliphate',
        type: 'Caliphate',
        layer_type: 'kingdoms',
        capital: 'Medina/Damascus',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [20.0, 15.0], [70.0, 15.0], [70.0, 42.0], [20.0, 42.0], [20.0, 15.0]
            ]]
        }
    },
    {
        start_year: 661,
        end_year: 750,
        name: 'Umayyad Caliphate',
        type: 'Caliphate',
        layer_type: 'kingdoms',
        capital: 'Damascus',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                // Iberia to Indus
                [-10.0, 10.0], [75.0, 10.0], [75.0, 45.0], [-10.0, 45.0], [-10.0, 10.0]
            ]]
        }
    },
    {
        start_year: 750,
        end_year: 1258,
        name: 'Abbasid Caliphate',
        type: 'Caliphate',
        layer_type: 'kingdoms',
        capital: 'Baghdad',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [25.0, 15.0], [75.0, 15.0], [75.0, 42.0], [25.0, 42.0], [25.0, 15.0]
            ]]
        }
    },
    {
        start_year: 1299,
        end_year: 1922,
        name: 'Ottoman Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Istanbul',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [15.0, 20.0], [55.0, 20.0], [55.0, 45.0], [15.0, 45.0], [15.0, 20.0]
            ]]
        }
    },

    // ====================================================================
    // INDIA (-322 to 1947 CE)
    // ====================================================================
    {
        start_year: -322,
        end_year: -185,
        name: 'Maurya Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Pataliputra',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [65.0, 8.0], [95.0, 8.0], [95.0, 35.0], [65.0, 35.0], [65.0, 8.0]
            ]]
        }
    },
    {
        start_year: 320,
        end_year: 550,
        name: 'Gupta Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Pataliputra',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [70.0, 15.0], [90.0, 15.0], [90.0, 30.0], [70.0, 30.0], [70.0, 15.0]
            ]]
        }
    },
    {
        start_year: 1526,
        end_year: 1857,
        name: 'Mughal Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Delhi/Agra',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [65.0, 8.0], [95.0, 8.0], [95.0, 35.0], [65.0, 35.0], [65.0, 8.0]
            ]]
        }
    },

    // ====================================================================
    // MEDIEVAL EUROPE (500 to 1500 CE)
    // ====================================================================
    {
        start_year: 800,
        end_year: 888,
        name: 'Carolingian Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Aachen',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [-5.0, 42.0], [15.0, 42.0], [15.0, 52.0], [-5.0, 52.0], [-5.0, 42.0]
            ]]
        }
    },
    {
        start_year: 962,
        end_year: 1806,
        name: 'Holy Roman Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Various',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [2.0, 43.0], [18.0, 43.0], [18.0, 55.0], [2.0, 55.0], [2.0, 43.0]
            ]]
        }
    },
    {
        start_year: 1000,
        end_year: 1789,
        name: 'Kingdom of France',
        type: 'Kingdom',
        layer_type: 'kingdoms',
        capital: 'Paris',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [-5.0, 42.0], [8.0, 42.0], [8.0, 51.0], [-5.0, 51.0], [-5.0, 42.0]
            ]]
        }
    },
    {
        start_year: 927,
        end_year: 1707,
        name: 'Kingdom of England',
        type: 'Kingdom',
        layer_type: 'kingdoms',
        capital: 'London',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [-6.0, 50.0], [2.0, 50.0], [2.0, 56.0], [-6.0, 56.0], [-6.0, 50.0]
            ]]
        }
    },

    // ====================================================================
    // MESOAMERICA (-2000 to 1521 CE)
    // ====================================================================
    {
        start_year: -2000,
        end_year: -400,
        name: 'Olmec Civilization',
        type: 'Civilization',
        layer_type: 'kingdoms',
        capital: 'Various',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [-96.0, 17.0], [-93.0, 17.0], [-93.0, 19.0], [-96.0, 19.0], [-96.0, 17.0]
            ]]
        }
    },
    {
        start_year: 250,
        end_year: 900,
        name: 'Maya Civilization (Classic)',
        type: 'City-States',
        layer_type: 'kingdoms',
        capital: 'Various',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [-93.0, 14.0], [-87.0, 14.0], [-87.0, 22.0], [-93.0, 22.0], [-93.0, 14.0]
            ]]
        }
    },
    {
        start_year: 1428,
        end_year: 1521,
        name: 'Aztec Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Tenochtitlan',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [-103.0, 16.0], [-96.0, 16.0], [-96.0, 22.0], [-103.0, 22.0], [-103.0, 16.0]
            ]]
        }
    },

    // ====================================================================
    // SOUTH AMERICA (1200 to 1533 CE)
    // ====================================================================
    {
        start_year: 1438,
        end_year: 1533,
        name: 'Inca Empire',
        type: 'Empire',
        layer_type: 'kingdoms',
        capital: 'Cusco',
        geometry: {
            type: 'Polygon',
            coordinates: [[
                [-82.0, -20.0], [-65.0, -20.0], [-65.0, 5.0], [-82.0, 5.0], [-82.0, -20.0]
            ]]
        }
    }
];

// Helper function to get boundaries for a specific year
function getHistoricalBoundariesForYear(year) {
    return HISTORICAL_BOUNDARIES
        .filter(boundary => year >= boundary.start_year && year <= boundary.end_year)
        .map(boundary => ({
            type: 'Feature',
            properties: {
                name: boundary.name,
                type: boundary.type,
                capital: boundary.capital || '',
                period: `${boundary.start_year < 0 ? Math.abs(boundary.start_year) + ' BCE' : boundary.start_year + ' CE'} - ${boundary.end_year < 0 ? Math.abs(boundary.end_year) + ' BCE' : boundary.end_year + ' CE'}`,
                layer_type: boundary.layer_type
            },
            geometry: boundary.geometry
        }));
}
