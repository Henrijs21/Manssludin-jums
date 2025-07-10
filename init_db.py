# init_db.py
import sqlite3
import json

DATABASE = 'mydatabase.db'

# Pilnīga kategoriju hierarhija un ar filtru grupu piesaisti
# Šie dati tiks ievietoti datubāzē
FULL_CATEGORY_DATA = {
    "Māja": {
        "Mēbeles": {
            "Dīvāni un atpūtas krēsli": {"filterGroup": "furniture-filters"},
            "Gultas un matrači": {"filterGroup": "furniture-filters"},
            "Skapji un kumodes": {"filterGroup": "furniture-filters"},
            "Galdi un krēsli": {"filterGroup": "furniture-filters"},
            "Plaukti": {"filterGroup": "furniture-filters"},
            "Bērnu mēbeles": {"filterGroup": "furniture-filters"},
            "Biroja mēbeles": {"filterGroup": "furniture-filters"},
            "Dārza mēbeles": {"filterGroup": "furniture-filters"},
            "Virtuves mēbeles": {"filterGroup": "furniture-filters"},
            "Citas mēbeles": {"filterGroup": "general-filters"}
        },
        "Sadzīves tehnika": {
            "Veļas mašīnas": {"filterGroup": "home-appliances-filters"},
            "Žāvētāji": {"filterGroup": "home-appliances-filters"},
            "Ledusskapji": {"filterGroup": "home-appliances-filters"},
            "Saldētavas": {"filterGroup": "home-appliances-filters"},
            "Plītis un cepeškrāsnis": {"filterGroup": "home-appliances-filters"},
            "Trauku mazgājamās mašīnas": {"filterGroup": "home-appliances-filters"},
            "Mazā virtuves tehnika": {"filterGroup": "home-appliances-filters"},
            "Putekļsūcēji": {"filterGroup": "home-appliances-filters"},
            "Gludekļi": {"filterGroup": "home-appliances-filters"},
            "Apkures ierīces": {"filterGroup": "home-appliances-filters"},
            "Gaisa kondicionieri": {"filterGroup": "home-appliances-filters"},
            "Cita sadzīves tehnika": {"filterGroup": "general-filters"}
        },
        "Virtuves piederumi un trauki": {"filterGroup": "general-filters"},
        "Tekstils un interjers": {"filterGroup": "general-filters"},
        "Apgaismojums": {"filterGroup": "general-filters"},
        "Dārzs un sēta": {"filterGroup": "general-filters"},
        "Santehnika un vannas istabas aprīkojums": {"filterGroup": "general-filters"},
        "Cits mājai": {"filterGroup": "general-filters"}
    },
    "Celtniecība": {
        "Celtniecības materiāli": {"filterGroup": "general-filters"},
        "Darbarīki": {"filterGroup": "tools-equipment-filters"},
        "Santehnika un apkure (celtniecības kontekstā)": {"filterGroup": "general-filters"},
        "Elektroinstalācija": {"filterGroup": "general-filters"},
        "Celtniecības tehnika": {"filterGroup": "tools-equipment-filters"},
        "Darba apģērbs un drošība": {"filterGroup": "clothing-filters"},
        "Cits celtniecībai": {"filterGroup": "general-filters"}
    },
    "Elektronika": {
        "Viedtālruņi un telefoni": {"filterGroup": "electronics-filters"},
        "Datori un biroja tehnika": {"filterGroup": "electronics-filters"},
        "Audio un video tehnika": {"filterGroup": "electronics-filters"},
        "Spēļu konsoles un spēles": {"filterGroup": "electronics-filters"},
        "Viedierīces un valkājamā elektronika": {"filterGroup": "electronics-filters"},
        "Biroja preces": {"filterGroup": "general-filters"},
        "Cita elektronika": {"filterGroup": "general-filters"}
    },
    "Apģērbs": {
        "Sievietēm": {"filterGroup": "clothing-filters"},
        "Vīriešiem": {"filterGroup": "clothing-filters"},
        "Bērniem (Apģērbs)": {"filterGroup": "clothing-filters"},
        "Sporta apģērbs": {"filterGroup": "clothing-filters"},
        "Apavi (vispārīgi)": {"filterGroup": "clothing-filters"},
        "Aksesuāri (vispārīgi)": {"filterGroup": "general-filters"}
    },
    "Bērniem": {
        "Bērnu transportlīdzekļi": {"filterGroup": "baby-items-filters"},
        "Bērnu mēbeles": {"filterGroup": "baby-items-filters"},
        "Rotaļlietas": {"filterGroup": "baby-items-filters"},
        "Barošana un aprūpe": {"filterGroup": "baby-items-filters"},
        "Grāmatas un mācību materiāli (bērniem)": {"filterGroup": "general-filters"},
        "Drošība bērniem": {"filterGroup": "general-filters"},
        "Cits bērniem": {"filterGroup": "general-filters"}
    },
    "Izklaide sports": {
        "Sports un fitnesa inventārs": {"filterGroup": "sports-leisure-filters"},
        "Mūzikas instrumenti un aprīkojums": {"filterGroup": "general-filters"},
        "Hobiji un amatniecība": {"filterGroup": "general-filters"},
        "Filmas, Mūzika, Grāmatas": {"filterGroup": "general-filters"},
        "Tūrisms un atpūta": {"filterGroup": "sports-leisure-filters"},
        "Medības un makšķerēšana": {"filterGroup": "sports-leisure-filters"},
        "Ballīšu un pasākumu preces": {"filterGroup": "general-filters"},
        "Cits izklaidei un sportam": {"filterGroup": "general-filters"}
    },
    "Dzīvnieki": {
        "Suņi": {"filterGroup": "animals-filters"},
        "Kaķi": {"filterGroup": "animals-filters"},
        "Mazie mājdzīvnieki (grauzēji, putni, zivis)": {"filterGroup": "animals-filters"},
        "Lauksaimniecības dzīvnieki (piederumi)": {"filterGroup": "animals-filters"},
        "Cits dzīvniekiem": {"filterGroup": "general-filters"}
    },
    "Transports": {
        "Vieglie auto": {"filterGroup": "transport-filters"},
        "Smagais transports": {"filterGroup": "general-filters"},
        "Motocikli un motorolleri": {"filterGroup": "general-filters"},
        "Velosipēdi": {"filterGroup": "general-filters"},
        "Laivas un ūdens transports": {"filterGroup": "general-filters"},
        "Rezerves daļas un aksesuāri (visiem transportlīdzekļiem, izņemot vieglos auto)": {"filterGroup": "general-filters"},
        "Cits transports": {"filterGroup": "general-filters"}
    },
    "Pakalpojumi": {
        "Remonts un uzstādīšana": {"filterGroup": "services-filters"},
        "Skaistumkopšana un veselība": {"filterGroup": "services-filters"},
        "Mācības un kursi": {"filterGroup": "services-filters"},
        "Noma": {"filterGroup": "services-filters"},
        "Pasākumu organizēšana": {"filterGroup": "services-filters"},
        "Tīrīšana un uzkopšana": {"filterGroup": "services-filters"},
        "Cits pakalpojumiem": {"filterGroup": "services-filters"}
    }
}

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            filter_group_id TEXT,
            display_order INTEGER DEFAULT 0,
            FOREIGN KEY (parent_id) REFERENCES categories (id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            category_id INTEGER NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            -- Common filter fields
            condition TEXT,
            brand TEXT,
            material TEXT,
            -- Electronics specific
            electronics_model TEXT,
            electronics_storage INTEGER,
            electronics_screen_size REAL,
            -- Clothing specific
            clothing_size TEXT,
            clothing_gender TEXT,
            clothing_season TEXT,
            -- Furniture specific
            furniture_color TEXT,
            furniture_style TEXT,
            furniture_dimensions TEXT,
            -- Home Appliances specific
            appliance_model TEXT,
            appliance_energy_class TEXT,
            appliance_capacity TEXT,
            -- Tools/Equipment specific
            tool_type TEXT,
            tool_power TEXT,
            -- Baby Items specific
            baby_age TEXT,
            baby_weight TEXT,
            -- Sports/Leisure specific
            sport_type TEXT,
            sport_size TEXT,
            -- Animals specific
            animal_type TEXT,
            animal_breed TEXT,
            animal_size TEXT,
            -- Services specific
            service_type TEXT,
            service_location TEXT,
            service_availability TEXT,
            -- Car specific (from existing form)
            car_brand TEXT,
            car_model TEXT,
            car_year_from INTEGER,
            car_year_to INTEGER,
            car_mileage INTEGER,
            car_extras TEXT, -- Storing as JSON string
            FOREIGN KEY (category_id) REFERENCES categories (id)
        );
    """)
    conn.commit()
    conn.close()

def populate_categories(data, parent_id=None, order=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    current_order = order

    for name, sub_data in data.items():
        filter_group = sub_data.get("filterGroup")
        
        cursor.execute("INSERT INTO categories (name, parent_id, filter_group_id, display_order) VALUES (?, ?, ?, ?)",
                       (name, parent_id, filter_group, current_order))
        new_id = cursor.lastrowid
        current_order += 1

        # If there are more nested subcategories (not just a filterGroup), recurse
        if isinstance(sub_data, dict) and not filter_group:
            populate_categories(sub_data, new_id, 0) # Reset order for sub-levels

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Initializing database...")
    create_tables()
    
    # Check if categories already exist to avoid duplicates
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM categories")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        print("Populating categories...")
        populate_categories(FULL_CATEGORY_DATA)
        print("Categories populated successfully.")
    else:
        print("Categories already exist in the database. Skipping population.")
    
    print("Database initialization complete.")
