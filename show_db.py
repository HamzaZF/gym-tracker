import sqlite3

DB_NAME = "seances.db"

def display_database():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Vérifier si la table "seances" existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='seances';")
        table_exists = cursor.fetchone()
        if not table_exists:
            print("La table 'seances' n'existe pas dans la base de données.")
            return
        
        # Récupérer le contenu de la table
        cursor.execute("SELECT * FROM seances")
        rows = cursor.fetchall()
        
        # Afficher les données
        if rows:
            print("Contenu de la table 'seances':")
            print("-" * 50)
            for row in rows:
                print(f"ID: {row[0]}, Date: {row[1]}, Jour: {row[2]}, Exercice: {row[3]}, Statut: {row[4]}")
            print("-" * 50)
        else:
            print("La table 'seances' est vide.")
    except sqlite3.Error as e:
        print(f"Une erreur s'est produite : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    display_database()
