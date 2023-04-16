import sqlite3

conn = sqlite3.connect('pictures.db')
cursor = conn.cursor()

# Création de la table Images
cursor.execute('''CREATE TABLE Images
                 (description text, url text)''')

# Insertion de quelques exemples d'images
images = [('Paysage de montagne', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Alpaca_-_panoramio_%28977%29.jpg/202px-Alpaca_-_panoramio_%28977%29.jpg'),
          ('Coucher de soleil', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Alpaca_-_panoramio_%28977%29.jpg/202px-Alpaca_-_panoramio_%28977%29.jpg'),
          ('Animal mignon', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Alpaca_-_panoramio_%28977%29.jpg/202px-Alpaca_-_panoramio_%28977%29.jpg')]

cursor.executemany("INSERT INTO Images (description, url) VALUES (?, ?)", images)

# Enregistrer les modifications
conn.commit()

# Fermer la connexion
conn.close()
