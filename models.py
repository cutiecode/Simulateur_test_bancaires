from flask_sqlalchemy import SQLAlchemy

# Déclaration de l'instance SQLAlchemy
db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    telephone = db.Column(db.String(20))
    date_naissance = db.Column(db.Date)
    adresse = db.Column(db.String(200))

    def __repr__(self):
        return f'<Client {self.client_id} >'

class Compte(db.Model):
    __tablename__ = 'comptes'

    compte_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'))
    solde = db.Column(db.Float)
    type_compte = db.Column(db.String(50))
    date_ouverture = db.Column(db.Date)
    plafond = db.Column(db.Float, default=10000.0)

    client = db.relationship('Client', backref=db.backref('comptes', lazy=True))

    def __repr__(self):
        return f'<Compte {self.compte_id}>'

class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('comptes.compte_id'))
    montant = db.Column(db.Float)
    type_transaction = db.Column(db.String(50))
    date_transaction = db.Column(db.Date)
    description = db.Column(db.String(200))
    status = db.Column(db.String(50))
    validation_message = db.Column(db.String(200))

    compte = db.relationship('Compte', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'

class TestResult(db.Model):
    __tablename__ = 'testresult'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'))
    result_status = db.Column(db.String(50))
    log_details = db.Column(db.Text)
    created_at = db.Column(db.Date)

    transaction = db.relationship('Transaction', backref=db.backref('test_results', lazy=True))

    def __repr__(self):
        return f'<TestResult {self.id}>'
