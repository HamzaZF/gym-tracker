from flask import Flask, redirect, render_template, url_for
import datetime
import sqlite3
from flask import request, jsonify
from flask import session

app = Flask(__name__)
app.secret_key = "03183142097209472"  # Remplacez par une clé secrète sécurisée

# Stockage temporaire pour simuler une validation
validation_status = {"validated": False, "day": None}

# Programme détaillé pour chaque jour
programmes = {
    'jour1': {
        'title': 'Jour 1 : Pectoraux et Triceps',
        'exercises': [
            {'name': 'Développé couché avec barre', 'sets': '5 séries x 6-8 reps', 'weight': '80 kg'},
            {'name': 'Développé incliné avec haltères', 'sets': '4 séries x 8-12 reps', 'weight': '25 kg par haltère'},
            {'name': 'Dips pour les pectoraux', 'sets': '4 séries x 10-12 reps', 'weight': '10 kg'},
            {'name': 'Extensions triceps à la poulie', 'sets': '4 séries x 12-15 reps', 'weight': '20 kg'},
            {'name': 'Pompes lestées', 'sets': '4 séries x 15-20 reps', 'weight': '10 kg'}
        ]
    },
    'jour2': {
        'title': 'Jour 2 : Dos et Biceps',
        'exercises': [
            {'name': 'Tractions larges', 'sets': '4 séries x max reps', 'weight': 'Poids de corps ou lest'},
            {'name': 'Rowing à la barre', 'sets': '4 séries x 8-10 reps', 'weight': '60 kg'},
            {'name': 'Tirage horizontal avec câble', 'sets': '4 séries x 12-15 reps', 'weight': '40 kg'},
            {'name': 'Curl incliné avec haltères', 'sets': '4 séries x 10-12 reps', 'weight': '12 kg par haltère'},
            {'name': 'Curl marteau', 'sets': '3 séries x 12-15 reps', 'weight': '15 kg'}
        ]
    },
    'jour3': {
        'title': 'Jour 3 : Épaules et Trapèzes',
        'exercises': [
            {'name': 'Développé militaire avec haltères', 'sets': '4 séries x 8-10 reps', 'weight': '20 kg par haltère'},
            {'name': 'Élévations latérales', 'sets': '4 séries x 12-15 reps', 'weight': '8 kg par haltère'},
            {'name': 'Rowing menton avec barre', 'sets': '4 séries x 10-12 reps', 'weight': '30 kg'},
            {'name': 'Shrugs avec haltères', 'sets': '4 séries x 15 reps', 'weight': '25 kg par haltère'},
            {'name': 'Face pulls', 'sets': '3 séries x 15 reps', 'weight': '20 kg'}
        ]
    },
    'jour4': {
        'title': 'Jour 4 : Entraînement Explosivité',
        'exercises': [
            {'name': 'Développé couché explosif', 'sets': '6 séries x 3 reps', 'weight': '60 kg avec élastiques'},
            {'name': 'Tirage explosif à la barre', 'sets': '5 séries x 5 reps', 'weight': '50 kg'},
            {'name': 'Pompes pliométriques', 'sets': '5 séries x 10-12 reps', 'weight': 'Poids de corps'},
            {'name': 'Med Ball Slam', 'sets': '4 séries x 15 reps', 'weight': '10 kg'}
        ]
    },
    'jour5': {
        'title': 'Jour 5 : Pectoraux et Dos',
        'exercises': [
            {'name': 'Développé décliné avec haltères', 'sets': '4 séries x 8-10 reps', 'weight': '25 kg par haltère'},
            {'name': 'Pull-over avec haltère', 'sets': '4 séries x 10-12 reps', 'weight': '20 kg'},
            {'name': 'Tractions en supination', 'sets': '4 séries x max reps', 'weight': 'Poids de corps ou assistance'},
            {'name': 'Rowing unilatéral avec haltère', 'sets': '4 séries x 10-12 reps', 'weight': '30 kg par haltère'},
            {'name': 'Push-up explosif sur banc', 'sets': '3 séries x 12-15 reps', 'weight': 'Poids de corps'}
        ]
    },
    'jour6': {
        'title': 'Jour 6 : Biceps, Triceps et Core',
        'exercises': [
            {'name': 'Curl barre EZ', 'sets': '4 séries x 8-10 reps', 'weight': '35 kg'},
            {'name': 'Curl concentré unilatéral', 'sets': '4 séries x 10-12 reps', 'weight': '15 kg'},
            {'name': 'Pompes diamant pour triceps', 'sets': '4 séries x 15 reps', 'weight': 'Poids de corps'},
            {'name': 'Skull Crushers avec haltères', 'sets': '4 séries x 8-10 reps', 'weight': '20 kg'},
            {'name': 'Planche lestée', 'sets': '4 séries x 60-90 secondes', 'weight': '10 kg'}
        ]
    },
    'jour7': {
        'title': 'Jour 7 : Repos ou Récupération Active',
        'exercises': [
            {'name': 'Stretching', 'details': '15-30 minutes de mobilité ou yoga.'},
            {'name': 'Massage ou Foam Rolling', 'details': 'Relâchement des tensions musculaires.'}
        ]
    }
}

def save_to_db(day, exercises):
    conn = sqlite3.connect("seances.db")
    c = conn.cursor()
    for exercise in exercises:
        c.execute("""
        INSERT INTO seances (date, day, exercise_name, status)
        VALUES (?, ?, ?, ?)
        """, (datetime.datetime.now().strftime("%Y-%m-%d"), day, exercise['name'], exercise['status']))
    conn.commit()
    conn.close()

@app.before_request
def initialize_session():
    if "validation_status" not in session:
        session["validation_status"] = {"validated": False, "day": None}

@app.cli.command('init-db')
def init_db():
    """Initialise la base de données."""
    from models import create_tables
    create_tables()
    print("Base de données initialisée.")

@app.route('/')
def accueil():
    today = datetime.datetime.now().weekday()
    day_mapping = {0: 'jour1', 1: 'jour2', 2: 'jour3', 3: 'jour4', 4: 'jour5', 5: 'jour6', 6: 'jour7'}
    current_day_key = day_mapping[today]

    if session["validation_status"]["validated"]:
        current_day_key = session["validation_status"]["day"]
    else:
        session["validation_status"]["day"] = current_day_key
        session.modified = True

    programme_du_jour = programmes[current_day_key]
    return render_template('index.html', programme=programme_du_jour, validation_status=session["validation_status"])


@app.route('/programme/<jour>')
def programme(jour):
    # Vérifiez si le jour existe dans le dictionnaire des programmes
    if jour in programmes:
        return render_template('programme.html', programme=programmes[jour])
    else:
        # Si le jour n'existe pas, renvoyer une page 404
        return render_template('404.html'), 404


@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    exercises = data.get('exercises', [])
    day = session["validation_status"]["day"]

    # Sauvegarder dans la base de données
    save_to_db(day, exercises)

    # Marquer comme validé
    session["validation_status"] = {"validated": True, "day": day}
    session.modified = True
    return jsonify({"message": "Séance validée et enregistrée avec succès !"})


@app.route('/reset', methods=['POST'])
def reset():
    if session["validation_status"]["validated"]:
        day = session["validation_status"]["day"]
        clear_selections_from_db(day)
    session["validation_status"] = {"validated": False, "day": None}
    session.modified = True
    return redirect(url_for('accueil'))

def clear_selections_from_db(day):
    """Supprime les sélections pour un jour spécifique dans la base de données."""
    conn = sqlite3.connect("seances.db")
    c = conn.cursor()
    c.execute("DELETE FROM seances WHERE day = ?", (day,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)