import sqlite3
import threading
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DATABASE = "pictures.db"

# Utilise threading.local() pour créer un objet de connexion différent pour chaque thread
connection = threading.local()

# Crée une fonction pour obtenir la connexion de la base de données
def get_db():
    if not hasattr(connection, "db"):
        connection.db = sqlite3.connect(DATABASE)
        connection.cursor_obj = connection.db.cursor()
    return connection.db, connection.cursor_obj






# Crée une fonction pour récupérer une image aléatoire depuis la base de données
def get_random_image():
    db, cursor = get_db()
    cursor.execute("SELECT * FROM Images ORDER BY RANDOM() LIMIT 1")
    return cursor.fetchone()

# Crée une route pour générer une image aléatoire
@app.route("/generate-image")
def generate_image():
    image = get_random_image()
    if image:
        return jsonify({
            "url": image[2],
            "description": image[1]
        })
    else:
        return "No images found in database"

# Crée une route pour afficher la page
@app.route("/")
def index():
    return render_template("hello.html")

# Crée une route pour ajouter une nouvelle image à la base de données
@app.route("/add-image", methods=["POST"])
def add_image():
    db, cursor = get_db()
    description = request.form.get("description")
    url = request.form.get("url")
    if description and url:
        cursor.execute("INSERT INTO Images (description, url) VALUES (?, ?)", (description, url))
        db.commit()
        return "Image added successfully"
    else:
        return "Please provide a description and a URL for the image"


@app.route("/show-image")
def show_image():
    image = get_random_image()
    if image:
        url = image[2]
        description = image[1]
        return render_template("image.html", url=url, description=description)
    else:
        return "No images found in database"

if __name__ == "__main__":
    # Crée la table Images si elle n'existe pas déjà
    conn, c = get_db()
    c.execute('''CREATE TABLE IF NOT EXISTS Images
                 (id INTEGER PRIMARY KEY,
                 description TEXT NOT NULL,
                 url TEXT NOT NULL)''')
    conn.commit()
    app.run(debug=True)
