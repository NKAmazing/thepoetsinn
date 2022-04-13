# Archivo para el recurso poemas

from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel


# Utilizo una clase Resources como recurso
class Poem(Resource):
    
    # Obtengo recurso
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()
    
    # Eliminar recurso
    def delete(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '', 204

    # Modificar recurso
    def put(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(poem, key, value)
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201


class Poems(Resource):
    # Obtener lista de poemas
    def get(self):
        poems = db.session.query(PoemModel).all()
        return jsonify([poem.to_json_short() for poem in poems])

    # Insertar recurso
    def post(self):
        # Obtener datos de la solicitud
        poem = PoemModel.from_json(request.get_json())
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201
        