# Archivo para el recurso puntuacion de los poemas

from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import RatingModel
from main.models import PoemModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.auth import decorators
from flask_mail import Mail
from main.mail.functions import sendMail


# Utilizo una clase Resources como recurso
class Rating(Resource):
    
    # Obtengo recurso
    def get(self, id):
        rating = db.session.query(RatingModel).get_or_404(id)
        return rating.to_json()
    
    # Eliminar recurso
    @jwt_required()
    def delete(self, id):
        current_identity = get_jwt_identity()
        rating = db.session.query(RatingModel).get_or_404(id)
        claims = get_jwt()
        # Verificar si el usuario es admin o el creador de la puntuacion
        if claims['role'] == "admin" or current_identity == rating.user_id:
            db.session.delete(rating)
            db.session.commit()
            return '', 204
        else:
            return 'This user is not allowed to do that.', 403

    # Modificar recurso
    @jwt_required()
    def put(self, id):
        current_identity = get_jwt_identity()
        claims = get_jwt()
        rating = db.session.query(RatingModel).get_or_404(id)
        # Verificar si el usuario es admin o el creador de la puntuacion
        if current_identity == rating.user_id:
            data = request.get_json().items()
            for key, value in data:
                setattr(rating, key, value)
            db.session.add(rating)
            db.session.commit()
            return rating.to_json(), 201
        else:
            return 'This user is not allowed to do that.', 403


class Ratings(Resource):

    # Obtener lista de puntuaciones
    def get(self):

        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "poem_id":
                    return self.show_ratings_by_poem_id(value)

        ratings = db.session.query(RatingModel).all()
        return jsonify([rating.to_json() for rating in ratings])
    
    # Insertar recurso
    @jwt_required()
    def post(self):
        current_identity = get_jwt_identity()
        # Obtener datos de la solicitud
        rating = RatingModel.from_json(request.get_json())
        rating.user_id = current_identity
        # Verificar si existe el poema
        db.session.query(PoemModel).get_or_404(rating.poem_id)
        # Agrega la calificacion
        db.session.add(rating)
        db.session.commit()
        sent = sendMail([rating.poem.user.email], "Your poem was rated!", 'rated', user = rating.poem.user, poem = rating.poem, user_1 = rating.user)
        return rating.to_json(), 201

    # Obtener lista de puntuaciones por id de poema
    def show_ratings_by_poem_id(self, id):
        ratings = db.session.query(RatingModel)
        ratings = ratings.filter(RatingModel.poem.has(PoemModel.id == id)).all()
        return jsonify([rating.to_json() for rating in ratings])