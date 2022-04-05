# Archivo para el recurso puntuacion de los poemas

from flask_restful import Resource
from flask import request

PUNCTUATIONS = {
    1: {'Score': '5', 'Comments': 'Awesome!'},
    2: {'Score': '4', 'Comments': 'So great!'}
}

# Utilizo una clase Resources como recurso
class Punctuation(Resource):
    
    # Obtengo recurso
    def get(self, id):
        # Verifico que existe una puntuacion con ese id
        if int(id) in PUNCTUATIONS:
            # Devuelvo puntuacion correspondiente
            return PUNCTUATIONS[int(id)]
        # Devuelvo error 404 en caso de no existir
        return '', 404
    
    # Eliminar recurso
    def delete(self, id):
        # Verifico que existe una puntuacion con ese id
        if int(id) in PUNCTUATIONS:
            # Elimino el archivo correspondiente
            del PUNCTUATIONS[int(id)]
            return '', 204
        # En caso de que no, retorno un 404
        return '', 404

    # Modificar recurso
    def put(self, id):
        if int(id) in PUNCTUATIONS:
            punct = PUNCTUATIONS[int(id)]
            # Obtengo los datos de la solicitud
            data = request.get_json()
            punct.update(data)
            return punct, 201
        # En caso de que no exista, retorno un 404
        return '', 404

class Punctuations(Resource):
    # Obtener lista de puntuaciones
    def get(self):
        return PUNCTUATIONS
    # Insertar recurso
    def post(self):
        # Obtener datos de la solicitud
        punct = request.get_json()
        id = int(max(PUNCTUATIONS.keys())) + 1
        PUNCTUATIONS[id] = punct
        return PUNCTUATIONS[id], 201
