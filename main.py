import sqlite3
import threading
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DATABASE = "pictures.db"
# Utilise threading.local() pour gérer le multi tâches
connection = threading.local()



#################################################################################################
##################################BASIC FUNCTION#################################################
#################################################################################################

# Crée une fonction pour obtenir la connexion de la base de données         // From tierce
def get_db():
    if not hasattr(connection, "db"):
        connection.db = sqlite3.connect(DATABASE)
        connection.cursor_obj = connection.db.cursor()
    return connection.db, connection.cursor_obj

def get_random_image():
    db, cursor = get_db()
    cursor.execute("SELECT * FROM Images ORDER BY RANDOM() LIMIT 1")
    return cursor.fetchone()


#################################################################################################
##################################BASIC FUNCTION#################################################
#################################################################################################







# Crée une route pour afficher la page
@app.route("/")
def index():
    return render_template("index.html")

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

# Crée une route pour ajouter une nouvelle image à la base de données
@app.route("/add-image", methods=["POST"])
def add_image():
    db, cursor = get_db()
    description = request.form.get("description")
    url = request.form.get("url")
    if description and url:
        cursor.execute("INSERT INTO Images (description, url) VALUES (?, ?)", (description, url))
        db.commit()
        return render_template("index.html", url=url, description=description)
    else:
        return "Renvoyer une description et un URL correct !"

@app.route("/show-image")
def show_image():
    image = get_random_image()
    if image:
        url = image[2]
        description = image[1]
        return render_template("random.html", url=url, description=description)
    else:
        return "Aucune image présente..."









#################################################################################################
#Initialisation de la base de donnée + création  de la table si elle n'existe pas
if __name__ == "__main__":
    # Crée la table Images si elle n'existe pas déjà
    conn, c = get_db()
    c.execute('''CREATE TABLE IF NOT EXISTS Images
                 (id INTEGER PRIMARY KEY,
                 description TEXT NOT NULL,
                 url TEXT NOT NULL)''')
    conn.commit()
    app.run(debug=True)
#################################################################################################