# Archivo para el recurso puntuacion de los poemas

from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import RatingModel
from main.models import PoemModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.auth import decorators


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
        if current_identity == rating.user_id:
            rating = db.session.query(RatingModel).get_or_404(id)
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
        ratings = db.session.query(RatingModel).all()
        return jsonify([rating.to_json() for rating in ratings])
    
    # Insertar recurso
    @jwt_required()
    def post(self):
        # Obtener datos de la solicitud
        rating = RatingModel.from_json(request.get_json())
        # Verificar si existe el usuario
        db.session.query(PoemModel).get_or_404(rating.poem_id)
        # Agrega la calificacion
        db.session.add(rating)
        db.session.commit()
        return rating.to_json(), 201
