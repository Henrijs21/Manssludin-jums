import sqlite3

# Izveido savienojumu ar datu bāzi (fails tiks izveidots, ja neeksistē)
connection = sqlite3.connect('database.db')

# Izveido kursoru, lai izpildītu SQL komandas
cursor = connection.cursor()

# SQL komanda, lai izveidotu tabulu
# Mēs pievienojam visus laukus no tavas `post-ad.html` formas
cursor.execute('''
CREATE TABLE IF NOT EXISTS ads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    company TEXT,
    price REAL,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Aizpildām datubāzi ar dažiem testa datiem, lai būtu ko filtrēt
# Vari pievienot vairāk datu, kopējot un mainot vērtības
test_ads = [
    ('maja', 'mebeles-un-interjers', 'Pārdod ozolkoka galdu', 'Lielisks stāvoklis, roku darbs.', 'Galdnieks SIA', 150.00, 'static/images/1.png'),
    ('elektronika', 'datori-un-piederumi', 'Lietots laptop Dell', 'Core i5, 8GB RAM, 256GB SSD. Der mācībām.', None, 250.50, 'static/images/3.png'),
    ('transports', 'vieglie-auto', 'VW Golf 5', '2008. gads, 1.9 TDI, labā tehniskā stāvoklī.', None, 2800.00, 'static/images/8.png'),
    ('celtnieciba', 'instrumenti', 'Bosch perforators', 'Jauns, iepakojumā. Varu nosūtīt ar pakomātu.', 'Instrumentu Noma', 85.00, 'static/images/2.png'),
    ('maja', 'majokla-iekartosana', 'Dekoratīvie spilveni', 'Komplekts no 3 spilveniem.', None, 20.00, 'static/images/1.png')
]

cursor.executemany('INSERT INTO ads (category, subcategory, title, description, company, price, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)', test_ads)


# Saglabā izmaiņas un aizver savienojumu
connection.commit()
connection.close()

print("Datu bāze 'database.db' un tabula 'ads' ir veiksmīgi izveidotas un aizpildītas ar testa datiem.")