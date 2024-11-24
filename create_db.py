import sqlite3

# Nom du fichier de base de données
DB_NAME = "seances.db"

def create_database():
    """Crée la base de données et la table `seances` avec les colonnes nécessaires."""
    conn = sqlite3.connect(DB_NAME)  # Connexion à la base de données
    c = conn.cursor()

    # Création de la table `seances` avec toutes les colonnes nécessaires
    c.execute("""
    CREATE TABLE IF NOT EXISTS seances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,            -- Date de la séance
        day TEXT NOT NULL,             -- Jour de la séance (e.g., jour1, jour2)
        exercise_name TEXT NOT NULL,   -- Nom de l'exercice
        weight REAL,                   -- Poids utilisé (optionnel pour certains exercices)
        min_reps INTEGER,              -- Nombre minimum de répétitions
        max_reps INTEGER,              -- Nombre maximum de répétitions
        status TEXT NOT NULL           -- Statut de l'exercice (Terminé ou Non Terminé)
    )
    """)

    conn.commit()  # Sauvegarde des modifications
    conn.close()   # Fermeture de la connexion
    print("Base de données créée avec succès.")

if __name__ == "__main__":
    create_database()
