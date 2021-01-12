#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, datetime, jwt, uuid
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from model import db, ma
from model import User, Tournee, PDI, UserSchema, TourneeSchema, PDISchema
import config

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.TRACK_MOD
app.config['SECRET_KEY'] = config.SECRET_KEY
# database init
#db = SQLAlchemy(app)
# marshmallow init
#ma = Marshmallow(app)
db.init_app(app)
ma.init_app(app)

# Init schema
pdi_schema = PDISchema()
pdis_schema = PDISchema(many=True)
tournee_schema = TourneeSchema()
tournees_schema = TourneeSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

'''
    Crée le wrapper token_required qui permettra de sécuriser certains appels à l'api
'''
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        # return f(current_user, *args, **kwargs)
        return f(*args, **kwargs)
    return decorator



# création d'une tournée
@app.route("/tournee", methods = ["POST"])
@token_required
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
@token_required
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
@token_required
def get_tournees():
    all_tournees = Tournee.query.all()
    result = tournees_schema.dump(all_tournees)
    return jsonify(result)


# get all pdis
@app.route("/pdi", methods = ["GET"])
@token_required
def get_pdis():
    all_pdis = PDI.query.all()
    result = pdis_schema.dump(all_pdis)
    return jsonify(result)



# get une tournée
@app.route("/tournee/<id>", methods = ["GET"])
@token_required
def get_tournee(id):
    tournee = Tournee.query.get(id)
    return tournee_schema.jsonify(tournee)


# get un pdi
@app.route("/pdi/<id>", methods = ["GET"])
@token_required
def get_pdi(id):
    pdi = PDI.query.get(id)
    return pdi_schema.jsonify(pdi)


#update une tournee
@app.route("/tournee/<id>", methods = ["PUT"])
@token_required
def update_tournee(id):
    tournee = Tournee.query.get(id)

    numero = request.json["numero"]
    date_crea = request.json["date_crea"]
    date_maj = request.json["date_maj"]

    tournee.numero = numero
    tournee.date_maj = datetime.datetime.now()

    db.session.commit()
    return tournee_schema.jsonify(tournee)

#update un pdi
@app.route("/pdi/<id>", methods = ["PUT"])
@token_required
def update_pdi(id):
    pdi = PDI.query.get(id)

    noms = request.json["noms"]
    adresse = request.json["adresse"]
    depot = request.json["depot"]
    tournee = request.json["tournee"]
    ordre = request.json["ordre"]
    date_crea = request.json["date_crea"]
    date_maj = request.json["date_maj"]

    pdi.noms = noms
    pdi.adresse = adresse
    pdi.depot = depot
    pdi.tournee = tournee
    pdi.ordre = ordre
    pdi.date_maj = datetime.datetime.now()

    db.session.commit()
    return pdi_schema.jsonify(pdi)


# delete tournee
@app.route("/tournee/<id>", methods = ["DELETE"])
@token_required
def delete_tournee(id):
    tournee = Tournee.query.get(id)
    db.session.delete(tournee)
    db.session.commit()

    return tournee_schema.jsonify(tournee)


# delete pdi
@app.route("/pdi/<id>", methods = ["DELETE"])
@token_required
def delete_pdi(id):
    pdi = PDI.query.get(id)
    db.session.delete(pdi)
    db.session.commit()

    return pdi_schema.jsonify(pdi)



# GET pdis par tournée order by ordre
@app.route("/tournee/<id>/pdis", methods = ["GET"])
@token_required
def get_pdis_from_tournee_orderby_ordre(id):
    pdis = PDI.query.filter_by(tournee = id).order_by(PDI.ordre).all()
    result = pdis_schema.dump(pdis)
    return jsonify(result)


# Register un nouvel utilisateur (ou mise à jour du mot de passe)
@app.route("/register", methods = ["POST", "GET"])
def register_user():
    data = request.get_json()

    # new_user_key = hashlib.pbkdf2_hmac('sha256', data["password"].encode("utf-8"), bytes(app.config['SECRET_KEY'], "utf-8"), 100000)
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(str(uuid.uuid4()), data['name'], hashed_password, data['admin'], datetime.datetime.now(), datetime.datetime.now())
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# connexion d'un utilisateur
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"message" : "could not login..."})

    user = User.query.filter_by(name=auth.username).first()

    #login_key = hashlib.pbkdf2_hmac('sha256', auth.password.encode('utf-8'), bytes(app.config['SECRET_KEY'], "utf-8"), 100000)
        
    if (check_password_hash(user.password, auth.password)):
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token' : bytes(token, "utf-8").decode('UTF-8')})

    return jsonify({"message" : "could not login..."})



# get la liste des utilisateurs
@app.route("/users", methods = ["GET"])
@token_required
def get_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)




def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
