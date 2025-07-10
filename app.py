import sqlite3
from flask import Flask, jsonify, render_template, request

# Inicializē Flask aplikāciju
app = Flask(__name__)

# Funkcija, lai pieslēgtos datu bāzei
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # Tas ļaus piekļūt kolonnām pēc nosaukuma
    return conn

# Maršruts, kas atgriezīs galveno lapu
@app.route('/')
def index():
    return render_template('index.html')

# API maršruts, kas atgriezīs sludinājumus (JSON formātā)
# Šo izmantos mūsu JavaScript, lai iegūtu datus
# Atrodi savu veco get_ads funkciju un aizstāj to ar šo jauno versiju
@app.route('/api/ads')
def get_ads():
    # Sākuma SQL vaicājums
    query = 'SELECT * FROM ads WHERE 1=1'
    params = []

    # Nolasa parametrus no URL (piem., /api/ads?category=maja)
    keyword = request.args.get('keyword')
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    # Dinamiski pievieno nosacījumus SQL vaicājumam
    if keyword:
        query += ' AND (title LIKE ? OR description LIKE ?)'
        # Pievienojam % zīmes, lai meklētu daļēju sakritību
        params.extend([f'%{keyword}%', f'%{keyword}%'])
    
    if category:
        query += ' AND category = ?'
        params.append(category)

    if min_price:
        query += ' AND price >= ?'
        params.append(float(min_price))

    if max_price:
        query += ' AND price <= ?'
        params.append(float(max_price))

    query += ' ORDER BY created_at DESC'

    # Izpilda SQL vaicājumu ar drošiem parametriem (tas novērš SQL injekcijas)
    conn = get_db_connection()
    ads = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify([dict(ad) for ad in ads])



@app.route('/profile')
def profile_page():
    return render_template('profile.html')
# Pievienojiet šo jauno funkciju savā app.py failā

@app.route('/iesniegt-sludinajumu')
def post_ad_page():
    # Šī funkcija renderē (parāda) jūsu post-ad.html lapu
    return render_template('post-ad.html')


# Nodrošina, ka serveris tiek palaists, tikai palaižot šo failu
if __name__ == '__main__':
    app.run(debug=True) # debug=True ļauj automātiski pārlādēt serveri pēc izmaiņām
