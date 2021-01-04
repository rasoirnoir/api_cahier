#!/usr/bin/env python

import os
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
    date_crea = db.Column(db.Date)
    date_maj = db.Column(db.Date)

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
    date_crea = db.Column(db.Date)
    date_maj = db.Column(db.Date)

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



# @app.route("/", methods=["GET"])
# def index():
#     return jsonify({"message": "Mauvaise route"})

def main():
    print("{} is running.".format(__file__.split("/")[len(__file__.split("/")) - 1]))
    app.run(debug=True)

if __name__ == "__main__":
    main()
