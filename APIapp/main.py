from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)
port = 3000
database = "kontakty.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                city VARCHAR(50) NOT NULL,
                phone_number VARCHAR(24) NOT NULL
            )
        ''')
        db.commit()

def check_api_status():
    return jsonify({"status": "API is running"}), 200

@app.route("/api/status", methods=["GET"])
def api_status():
    return check_api_status()

@app.route("/api/contacts", methods=["POST"])
def add_contact():
    data = request.json
    for key, value in data.items():
        if value == "":
            return jsonify({"error": f"{key} cannot be empty"}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO contacts (first_name, last_name, city, phone_number) VALUES (?, ?, ?, ?) 
    ''', (data["first_name"], data["last_name"], data["city"], data["phone_number"]))

    db.commit()
    contact_id = cursor.lastrowid

    return jsonify({"message": "Contact added successfully", "contactId": contact_id}), 201


@app.route("/api/contacts", methods=["GET"])
def get_all_contacts():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    return jsonify(contacts)

@app.route("/api/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    contact = cursor.fetchone()

    if contact:
        return jsonify(contact)
    else:
        return jsonify({"error": "Contact not found"}), 404

@app.route("/api/contacts/<int:contact_id>", methods=["PATCH"])
def update_contact(contact_id):
    new_data = request.json
    for key, value in new_data.items():
        if value == "":
            return jsonify({"error": f"{key} cannot be empty"}), 400
    update_fields = ', '.join([f'{key} = ?' for key in new_data.keys()])
    query = f'''
        UPDATE contacts SET {update_fields} WHERE id = ?
    '''
    values = list(new_data.values()) + [contact_id]

    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Contact updated successfully"})

@app.route("/api/contacts/<int:contact_id>", methods=["PUT"])
def replace_contact(contact_id):
    new_data = request.json

    for key, value in new_data.items():
        if value == "":
            return jsonify({"error": f"{key} cannot be empty"}), 400
        
    if "first_name" not in new_data or "last_name" not in new_data or "city" not in new_data or "phone_number" not in new_data:
        return jsonify({"error": "Contact data missing."}), 400

    query = '''
        UPDATE contacts SET first_name = ?, last_name = ?, city = ?, phone_number = ? WHERE id = ?
    '''
    values = [new_data["first_name"], new_data["last_name"], new_data["city"], new_data["phone_number"], contact_id]

    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Contact updated successfully"}), 204

@app.route("/api/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    row = cursor.fetchone()

    if not row:
        return jsonify({"error": "Contact not found"}), 404

    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    db.commit()

    return jsonify({"message": "Contact deleted successfully"})

if __name__ == "__main__":
    init_db()
    app.run(port=port)
