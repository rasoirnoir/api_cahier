from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


# class PDI
class PDI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    noms = db.Column(db.String)
    adresse = db.Column(db.String, nullable=False)
    depot = db.Column(db.Boolean)
    tournee = db.Column(db.Integer, db.ForeignKey('tournee.id'), nullable=True)
    ordre = db.Column(db.Integer)
    date_crea = db.Column(db.DateTime)
    date_maj = db.Column(db.DateTime)

    def __init__(self, noms, adresse, depot, tournee, ordre, date_crea, date_maj):
        self.noms = noms
        self.adresse = adresse
        self.depot = depot
        self.tournee = tournee
        self.ordre = ordre
        self.date_crea = date_crea
        self.date_maj = date_maj

#class Tournee
class Tournee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True)
    # pdis = db.Relationship('PDI', backref='pdi', lazy=True)
    date_crea = db.Column(db.DateTime)
    date_maj = db.Column(db.DateTime)

    def __init__(self, numero, date_crea, date_maj):
        self.numero = numero
        self.date_crea = date_crea
        self.date_maj = date_maj
    

# Classe User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    #password = db.Column(db.String(50))
    password = db.Column(db.String)
    admin = db.Column(db.Boolean)
    date_crea = db.Column(db.DateTime)
    date_maj = db.Column(db.DateTime)

    def __init__(self, public_id, name, password, admin, date_crea, date_maj):
        self.public_id = public_id
        self.name = name
        self.password = password
        self.admin = admin
        self.date_crea = date_crea
        self.date_maj = date_maj




#PDI schema
class PDISchema(ma.Schema):
    class Meta:
        fields = ('id', 'noms', 'adresse', 'depot', 'tournee', 'ordre', 'date_crea', 'date_maj')

#Tournee schema
class TourneeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'numero', 'date_crea', 'date_maj')



#User schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'name', 'password', 'admin', 'date_crea', 'date_maj')
