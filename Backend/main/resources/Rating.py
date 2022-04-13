# Archivo para el recurso puntuacion de los poemas

from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import RatingModel


# Utilizo una clase Resources como recurso
class Rating(Resource):
    
    # Obtengo recurso
    def get(self, id):
        rating = db.session.query(RatingModel).get_or_404(id)
        return rating.to_json()
    
    # Eliminar recurso
    def delete(self, id):
        rating = db.session.query(RatingModel).get_or_404(id)
        db.session.delete(rating)
        db.session.commit()
        return '', 204

    # Modificar recurso
    def put(self, id):
        rating = db.session.query(RatingModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(rating, key, value)
            db.session.add(rating)
            db.session.commit()
            return rating.to_json(), 201


class Ratings(Resource):
    # Obtener lista de puntuaciones
    def get(self):
        ratings = db.session.query(RatingModel).all()
        return jsonify([rating.to_json_short() for rating in ratings])

    # Insertar recurso
    def post(self):
        rating = RatingModel.from_json(request.get_json())
        db.session.add(rating)
        db.session.commit()
        return rating.to_json(), 201
