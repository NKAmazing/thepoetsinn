# Archivo para el recurso usuarios

from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel

# USERS = {
#     1: {'Username': 'Nicolas', 'Password': '1234'},
#     2: {'Username': 'Alexis', 'Password': '5678'}
# }

# Utilizo una clase Resources como recurso
class User(Resource):
    
    # Obtengo recurso
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()
        
    
    # Eliminar recurso
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    # Modificar recurso
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json() , 201


class Users(Resource):
    # Obtener lista de usuarios
    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify([user.to_json_short() for user in users])

    """
            list_user = []
            for user in users:
                list_user.append(user.to_json())
            return jsonify(list_user)
    """


    # Insertar recurso
    def post(self):
        # Obtener datos de la solicitud
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
