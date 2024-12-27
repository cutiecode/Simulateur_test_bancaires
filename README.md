# Simulateur de Validation de Transactions avec Exportation de Logs

Ce projet est une application web développée avec **Flask** qui sert de simulateur de test pour valider des transactions bancaires dans un environnement simulé. Inspirée des outils de gestion de tests comme **HP ALM**, l'application permet de tester l'intégration des transactions et d'enregistrer des logs détaillés d'activité. Elle offre également la possibilité d'exporter ces logs sous forme de fichiers Excel pour un suivi et une analyse ultérieurs.

## Objectif

L'objectif de ce projet est de simuler et de valider des transactions bancaires dans un environnement de test. Il permet de superviser, tester et analyser les transactions avant leur déploiement en production, dans le but d'assurer leur bon fonctionnement. Ce système est conçu pour être facilement adaptable aux besoins de simulation de tests dans un cadre bancaire ou financier.

## Fonctionnalités

- **Validation des transactions bancaires** : Effectue des transactions de type dépôt ou retrait, en validant les informations telles que l'ID du compte, le type de transaction et le montant.
- **Exportation des logs** : Permet d'exporter les logs d'activité sous forme de fichier Excel pour un suivi détaillé des transactions.
- **Vérification de la base de données** : Vérifie la connexion à la base de données pour assurer son bon fonctionnement avant de procéder aux transactions.
- **Simulateur d'environnement de test** : Permet de tester l'intégration des transactions dans un environnement simulé, idéal pour la préparation des tests ou pour valider des processus avant la production.

## Prérequis

Avant de commencer, assurez-vous que vous avez les éléments suivants installés sur votre machine :

- Python 3.7 ou supérieur
- MySQL ou MariaDB pour la gestion de la base de données
- Pip (gestionnaire de paquets Python)

## Installation

1. Clonez ce repository sur votre machine locale :
   ```bash
   git clone https://github.com/ton-utilisateur/ton-repository.git
   cd ton-repository

2. Créez un environnement virtuel pour le projet :

python -m venv venv
source venv/bin/activate  # Sur Windows : Créez un environnement virtuel pour le projet :

3. Créez un fichier .env à la racine du projet pour définir les variables d'environnement suivantes :

SECRET_KEY=ta_cle_secrete
MYSQL_USER=ton_utilisateur_mysql
MYSQL_PASSWORD=ton_mot_de_passe_mysql
MYSQL_HOST=localhost
MYSQL_DB=nom_de_ta_base_de_donnees

Pour démarrer l'application, utilisez la commande suivante dans votre terminal : 
python app.py

## Routes disponibles 

1. / : Page d'accueil de l'application.

2. /check-db : Vérifie la connexion à la base de données. Retourne un message de succès ou d'erreur.

3. /transaction : Reçoit une requête POST pour effectuer une transaction bancaire (retrait ou dépôt). Les données doivent être envoyées en format JSON. 

4. /creer_transaction : Crée une nouvelle transaction (retrait ou dépôt). Les données doivent être envoyées en format JSON.

5. /export_logs : Exporte les logs de l'application sous forme de fichier Excel.

## Exemple de requêtes

1. POST /transaction :
{
  "compte_id": 123,
  "type_transaction": "retrait",
  "montant": 200.0
}

2. POST /creer_transaction :
{
  "compte_id": 456,
  "type_transaction": "depot",
  "transaction_date": "2024-12-27",
  "montant": 150.0
}

3. GET /export_logs : Télécharge le fichier Excel des logs de l'application.

## Technologies utilisées

1. Flask : Framework web pour Python.

2. SQLAlchemy : ORM pour la gestion de la base de données MySQL.

3. MySQL : Système de gestion de base de données relationnelle.

4. Python-dotenv : Permet de gérer les variables d'environnement.

## Contribuer

Les contributions sont les bienvenues ! Si vous souhaitez proposer des améliorations ou corriger des bugs, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## License

Ce projet est sous licence MIT.