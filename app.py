#!/usr/bin/env python

import os, datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# database init
db = SQLAlchemy(app)
# marshmallow init
ma = Marshmallow(app)

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

#PDI schema
class PDISchema(ma.Schema):
    class Meta:
        fields = ('id', 'noms', 'adresse', 'depot', 'tournee', 'ordre', 'date_crea', 'date_maj')

#Tournee schema
class TourneeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'numero', 'date_crea', 'date_maj')


# Init schema
pdi_schema = PDISchema()
pdis_schema = PDISchema(many=True)
tournee_schema = TourneeSchema()
tournees_schema = TourneeSchema(many=True)

# création d'une tournée
@app.route("/tournee", methods = ["POST"])
def add_tournee():
    numero = request.json["numero"]
    date_crea = datetime.datetime.now()
    date_maj = datetime.datetime.now()

    new_tournee = Tournee(numero, date_crea, date_maj)
    db.session.add(new_tournee)
    db.session.commit()

    return tournee_schema.jsonify(new_tournee)

# création d'un pdi
@app.route("/pdi", methods = ["POST"])
def add_pdi():
    noms = request.json["noms"]
    adresse = request.json["adresse"]
    depot = request.json["depot"]
    tournee = request.json["tournee"]
    ordre = request.json["ordre"]
    date_crea = datetime.datetime.now()
    date_maj = datetime.datetime.now()

    new_pdi = PDI(noms, adresse, depot, tournee, ordre, date_crea, date_maj)
    db.session.add(new_pdi)
    db.session.commit()

    return pdi_schema.jsonify(new_pdi)


# get all tournées
@app.route("/tournee", methods = ["GET"])
def get_tournees():
    all_tournees = Tournee.query.all()
    result = tournee_schema.dump(all_tournees)
    return jsonify(result)






def main():
    print("{} is running.".format(__file__.split("/")[len(__file__.split("/")) - 1]))
    app.run(debug=True)

if __name__ == "__main__":
    main()
