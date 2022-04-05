# Archivo para el recurso poemas

from flask_restful import Resource
from flask import request

POEMS = {
    1: {'Name': 'First Poem'},
    2: {'Name': 'Second Poem'}
}

# Utilizo una clase Resources como recurso
class Poem(Resource):
    
    # Obtengo recurso
    def get(self, id):
        # Verifico que existe un poema con ese id
        if int(id) in POEMS:
            # Devuelvo poema correspondiente
            return POEMS[int(id)]
        # Devuelvo error 404 en caso de no existir
        return '', 404
    
    # Eliminar recurso
    def delete(self, id):
        # Verifico que existe un poema con ese id
        if int(id) in POEMS:
            # Elimino el archivo correspondiente
            del POEMS[int(id)]
            return '', 204
        # En caso de que no, retorno un 404
        return '', 404

    # Modificar recurso
    def put(self, id):
        if int(id) in POEMS:
            poem = POEMS[int(id)]
            # Obtengo los datos de la solicitud
            data = request.get_json()
            poem.update(data)
            return poem, 201
        # En caso de que no exista, retorno un 404
        return '', 404

class Poems(Resource):
    # Obtener lista de poemas
    def get(self):
        return POEMS
    # Insertar recurso
    def post(self):
        # Obtener datos de la solicitud
        poem = request.get_json()
        id = int(max(POEMS.keys())) + 1
        POEMS[id] = poem
        return POEMS[id], 201
           
        