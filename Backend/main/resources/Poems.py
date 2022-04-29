# Archivo para el recurso poemas

from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel
from main.models import UserModel
from main.models import RatingModel
from datetime import datetime
from sqlalchemy import func


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
        poems = db.session.query(PoemModel)
        page = 1
        perpage = 5
        if request.get_json():
            # declaro un request de items como filters
            filters = request.get_json().items()
            for key, value in filters:
                # itero con un if, todos los filtros correspondientes
                if key == "page":
                    page = int(value)
                if key == "perpage":
                    perpage = int(value)
                if key == "title":
                    poems = poems.filter(PoemModel.title.like("%" + value + "%"))
                if key == "user_id":
                    poems = poems.filter(PoemModel.user_id == value)
                if key == "date_time[gte]":
                    poems = poems.filter(PoemModel.date_time >= datetime.strptime(value, '%d-%m-%Y'))
                if key == "date_time[lte]":
                    poems = poems.filter(PoemModel.date_time <= datetime.strptime(value, '%d-%m-%Y'))
                if key == "username":
                    poems = poems.filter(PoemModel.user.has(UserModel.username.like("%" + value + "%")))
                # agrego el sort by
                if key == "sort_by":
                    # ordeno por fecha
                    if value == "date_time":
                        poems = poems.order_by(PoemModel.date_time)
                    if value == "date_time[desc]":
                        poems = poems.order_by(PoemModel.date_time.desc())
                    if value == "rating":
                        # utilizo un outerjoin y luego un group by para obtener las calificaciones del poema, luego hago un promedio
                        poems = poems.outerjoin(PoemModel.ratings).group_by(PoemModel.id).order_by(func.avg(RatingModel.score))
                    if value == "rating[desc]":
                        # misma operacion pero ahora en modo descendente
                        poems = poems.outerjoin(PoemModel.ratings).group_by(PoemModel.id).order_by(func.avg(RatingModel.score).desc())
        # hago el paginado de poemas pasandole la pagina y la cantidad de poemas por pagina, luego establezco un limite de poemas por pagina          
        poems = poems.paginate(page, perpage, True, 10)
        # retorno el to json short, el total de poemas y la pagina
        return jsonify({"poems":[poem.to_json_short() for poem in poems.items],
        "total": poems.total, "pages": poems.pages, "page": page})

    # Insertar recurso
    def post(self):
        # Obtener datos de la solicitud
        poem = PoemModel.from_json(request.get_json())
        # Verificar si existe el usuario
        db.session.query(UserModel).get_or_404(poem.user_id)
        # Agrega el poema
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201
        