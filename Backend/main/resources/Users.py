# Archivo para el recurso usuarios

from flask_restful import Resource
from flask import request

USERS = {
    1: {'Username': 'Nicolas', 'Password': '1234'},
    2: {'Username': 'Alexis', 'Password': '5678'}
}

# Utilizo una clase Resources como recurso
class User(Resource):
    
    # Obtengo recurso
    def get(self, id):
        # Verifico que existe un usuario con ese id
        if int(id) in USERS:
            # Devuelvo usuario correspondiente
            return USERS[int(id)]
        # Devuelvo error 404 en caso de no existir
        return '', 404
    
    # Eliminar recurso
    def delete(self, id):
        # Verifico que existe un usuario con ese id
        if int(id) in USERS:
            # Elimino el usuario correspondiente
            del USERS[int(id)]
            return '', 204
        # En caso de que no, retorno un 404
        return '', 404

    # Modificar recurso
    def put(self, id):
        if int(id) in USERS:
            user = USERS[int(id)]
            # Obtengo los datos de la solicitud
            data = request.get_json()
            user.update(data)
            return user, 201
        # En caso de que no exista, retorno un 404
        return '', 404

class Users(Resource):
    # Obtener lista de usuarios
    def get(self):
        return USERS
    # Insertar recurso
    def post(self):
        # Obtener datos de la solicitud
        user = request.get_json()
        id = int(max(USERS.keys())) + 1
        USERS[id] = user
        return USERS[id], 201
