# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import json
import os

app = Flask(__name__)

DATABASE = 'mydatabase.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

# API Endpoints

@app.route('/api/categories', methods=['GET'])
def get_main_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories WHERE parent_id IS NULL ORDER BY display_order")
    main_categories = [{"id": row['id'], "name": row['name']} for row in cursor.fetchall()]
    conn.close()
    return jsonify(main_categories)

@app.route('/api/categories/<int:parent_id>/subcategories', methods=['GET'])
def get_subcategories(parent_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, filter_group_id FROM categories WHERE parent_id = ? ORDER BY display_order", (parent_id,))
    subcategories = []
    for row in cursor.fetchall():
        subcategories.append({
            "id": row['id'],
            "name": row['name'],
            "filterGroup": row['filter_group_id'] # This can be None if not a leaf node
        })
    conn.close()
    return jsonify(subcategories)

@app.route('/api/ads', methods=['POST'])
def create_ad():
    data = request.json
    
    # Basic validation (extend as needed)
    required_fields = ['title', 'description', 'price', 'category_id']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Collect all possible filter fields from the request data
        # This is a simplified approach; in a real app, you'd map these carefully
        ad_data = {
            "title": data.get('title'),
            "description": data.get('description'),
            "price": data.get('price'),
            "category_id": data.get('category_id'),
            "image_url": data.get('image', None), # 'image' is the name in the form
            "condition": data.get('item_condition', None),
            "brand": data.get('item_brand', None),
            "material": data.get('item_material', None),
            "electronics_model": data.get('electronics_model', None),
            "electronics_storage": data.get('electronics_storage', None),
            "electronics_screen_size": data.get('electronics_screen_size', None),
            "clothing_size": data.get('clothing_size', None),
            "clothing_gender": data.get('clothing_gender', None),
            "clothing_season": data.get('clothing_season', None),
            "furniture_color": data.get('furniture_color', None),
            "furniture_style": data.get('furniture_style', None),
            "furniture_dimensions": data.get('furniture_dimensions', None),
            "appliance_model": data.get('appliance_model', None),
            "appliance_energy_class": data.get('appliance_energy_class', None),
            "appliance_capacity": data.get('appliance_capacity', None),
            "tool_type": data.get('tool_type', None),
            "tool_power": data.get('tool_power', None),
            "baby_age": data.get('baby_age', None),
            "baby_weight": data.get('baby_weight', None),
            "sport_type": data.get('sport_type', None),
            "sport_size": data.get('sport_size', None),
            "animal_type": data.get('animal_type', None),
            "animal_breed": data.get('animal_breed', None),
            "animal_size": data.get('animal_size', None),
            "service_type": data.get('service_type', None),
            "service_location": data.get('service_location', None),
            "service_availability": data.get('service_availability', None),
            "car_brand": data.get('car_brand', None),
            "car_model": data.get('car_model', None),
            "car_year_from": data.get('car_year_from', None),
            "car_year_to": data.get('car_year_to', None),
            "car_mileage": data.get('car_mileage', None),
            "car_extras": json.dumps(data.get('car_extras', [])) # Store list of extras as JSON string
        }

        # Construct the SQL query dynamically based on provided fields
        columns = ', '.join(ad_data.keys())
        placeholders = ', '.join(['?' for _ in ad_data.keys()])
        values = tuple(ad_data.values())

        cursor.execute(f"INSERT INTO ads ({columns}) VALUES ({placeholders}) RETURNING id", values)
        ad_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Sludinājums veiksmīgi pievienots!", "ad_id": ad_id}), 201
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/ads', methods=['GET'])
def get_ads():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Join with categories to get category name
    cursor.execute("""
        SELECT a.*, c.name as category_name
        FROM ads a
        JOIN categories c ON a.category_id = c.id
        ORDER BY a.created_at DESC
    """)
    ads = []
    for row in cursor.fetchall():
        ad = dict(row)
        if ad['car_extras']:
            ad['car_extras'] = json.loads(ad['car_extras']) # Convert JSON string back to list
        ads.append(ad)
    conn.close()
    return jsonify(ads)


# Serve HTML templates
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iesniegt-sludinajumu')
def post_ad_page():
    return render_template('post-ad.html') # Note: file name is post-ad.html

# Serve static files (like car_data.json)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Ensure the database is initialized before running the app
    # In a production environment, this would be handled by a separate deployment step
    # For this demo, we'll run init_db.py logic here or instruct user to run it first.
    # It's safer to instruct the user to run init_db.py manually once.
    print("Starting Flask application. Ensure 'init_db.py' has been run to create the database.")
    app.run(debug=True) # debug=True for development, disable in production
