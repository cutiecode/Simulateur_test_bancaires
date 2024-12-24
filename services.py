import pandas as pd
from models import db, Compte, Transaction, TestResult
from datetime import datetime

def valider_transaction(compte_id, type_transaction, montant):
    try:
        # Rechercher le compte par ID
        compte = Compte.query.filter_by(compte_id=compte_id).first()

        if not compte:
            return {"status": "Échec", "message": "Compte introuvable"}

        if type_transaction == "retrait":
            if compte.solde >= montant:
                compte.solde -= montant
                statut = "validé"
                message = "Retrait réussi"
            else:
                statut = "échoué"
                message = "Solde insuffisant"
        elif type_transaction == "depot":
            if (compte.solde + montant) <= compte.plafond:
                compte.solde += montant
                statut = "validé"
                message = "Dépôt réussi"
            else:
                statut = "échoué"
                message = "Plafond dépassé"
        else:
            statut = "échoué"
            message = "Type de transaction invalide"

        # Ajouter une nouvelle transaction dans la base de données
        nouvelle_transaction = Transaction(
            compte_id=compte_id,
            montant=montant,
            type_transaction=type_transaction,
            date_transaction=date.now(),  # Utilisez `date.today()` pour obtenir la date actuelle
            status=statut,
            validation_message=message
        )

        # Debug: afficher les informations de la transaction avant commit
        print(f"Transaction à ajouter : {nouvelle_transaction}")

        # Ajouter et valider la transaction dans la base de données
        db.session.add(nouvelle_transaction)
        db.session.commit()

        # Ajouter un résultat de test dans la table 'TestResult'
        log_message = f"Transaction {statut}: {message}"
        test_result = TestResult(
            transaction_id=nouvelle_transaction.transaction_id,
            result_status=statut,
            log_details=log_message,
            created_at=date.now()  # Date et heure actuelles pour le log
        )

        # Ajouter le résultat de test à la base de données
        db.session.add(test_result)
        db.session.commit()

        print(f"Transaction {statut} : {message} ajoutée avec succès.")
        return {"status": statut, "message": message}

    except Exception as e:
        db.session.rollback()  # Annuler la transaction en cas d'erreur
        print(f"Erreur de transaction : {str(e)}")
        return {"status": "Échec", "message": f"Erreur de transaction : {str(e)}"}


def exporter_logs():
    try:
        # Récupérer les logs depuis la table TestResult
        logs = TestResult.query.all()

        # Vérifier si des logs ont été trouvés
        if not logs:
            raise Exception("Aucun log trouvé à exporter.")

        # Convertir les logs en DataFrame
        result_data = []
        for result in logs:
            result_data.append({
                'id': result.id,
                'transaction_id': result.transaction_id,
                'result_status': result.result_status,
                'log_details': result.log_details,
                'created_at': result.created_at
            })

        # Créer un DataFrame à partir des logs
        df = pd.DataFrame(result_data)

        # Définir le chemin du fichier Excel
        file_path = "logs_export.xlsx"

        # Exporter le DataFrame en fichier Excel
        df.to_excel(file_path, index=False)

        # Retourner le chemin du fichier
        return file_path

    except Exception as e:
        print(f"Erreur lors de l'exportation des logs : {str(e)}")
        return None
