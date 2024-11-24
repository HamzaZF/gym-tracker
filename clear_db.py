import sqlite3

DB_NAME = "seances.db"

def clear_database():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Supprimer toutes les données des tables
        cursor.execute("DELETE FROM seances")
        conn.commit()
        
        print("La base de données a été nettoyée avec succès.")
    except sqlite3.Error as e:
        print(f"Une erreur s'est produite : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clear_database()
