from flask import Flask, request, render_template, jsonify, send_file
from models import db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from services import valider_transaction, exporter_logs
from sqlalchemy import text
import os
from datetime import datetime, date

load_dotenv()

# Initialisation de l'application Flask
app = Flask(__name__)

# Configurer l'application avec les variables d'environnement
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}" # Initialiser SQLAlchemy avec l'application 
db.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-db')
def check_db():
    try:
        # Tester la connexion à la base de données
        db.session.execute(text('SELECT 1'))
        return "Connexion à la base de données réussie !", 200
    except Exception as e:
        return f"Erreur de connexion : {str(e)}", 500

@app.route('/transaction', methods=['POST'])
def effectuer_transaction():
    # Vérifier si les champs nécessaires sont présents
    if not request.json:
        return jsonify({"status": "Échec", "message": "Aucune donnée reçue"}), 400
    data = request.json
    print("Données reçues:", data)  # Ajoutez cette ligne pour inspecter les données
    
    if 'compte_id' not in data:
        return jsonify({"status": "Échec", "message": "Champ 'compte_id' manquant"}), 400
    if 'type_transaction' not in data:
        return jsonify({"status": "Échec", "message": "Champ 'type_transaction' manquant"}), 400
    if 'montant' not in data:
        return jsonify({"status": "Échec", "message": "Champ 'montant' manquant"}), 400

    # Récupérer les données du formulaire
    compte_id = data['compte_id']
    type_transaction = data['type_transaction']
    montant = data['montant']

    # Validation des données
    if not isinstance(compte_id, int):
        return jsonify({"status": "Échec", "message": "L'ID du compte doit être un entier"}), 400
    if type_transaction not in ['retrait', 'depot']:
        return jsonify({"status": "Échec", "message": "Type de transaction invalide"}), 400
    try:
        montant = float(montant)
        if montant <= 0:
            raise ValueError("Montant négatif ou nul")
    except ValueError:
        return jsonify({"status": "Échec", "message": "Montant invalide"}), 400

    # Appeler la fonction de service pour valider la transaction
    resultat = valider_transaction(compte_id, type_transaction, montant)

    # Retourner la réponse JSON
    return jsonify(resultat)


@app.route('/creer_transaction', methods=['POST'])
def nouvelle_transaction():
    data = request.json
    compte_id = data.get('compte_id')
    type_transaction = data.get('type_transaction')
    date_transaction = data.get('transaction_date', date.today())
    montant = data.get('montant')

    # Appeler la fonction pour valider la transaction
    resultat = valider_transaction(compte_id, type_transaction, montant)
    return jsonify(resultat)

@app.route('/export-logs', methods=['GET'])
def export_logs():
    try:
        # Appeler la fonction pour exporter les logs
        file_path = exporter_logs()

        # Retourner le fichier Excel en tant que téléchargement
        return send_file(file_path, as_attachment=True, download_name='logs_export.xlsx')

    except Exception as e:
        return f"Erreur lors de l'exportation des logs : {str(e)}", 500

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
