# Archivo para el recurso poemas

from itertools import count
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel
from main.models import UserModel
from main.models import RatingModel
from datetime import datetime
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.auth import decorators


# Utilizo una clase Resources como recurso
class Poem(Resource):
    
    # Obtengo recurso
    @jwt_required(optional=True)
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        # Verificar si se ha ingresado con token
        current_identity = get_jwt_identity()
        if current_identity:
            return poem.to_json()
        else:
            return poem.to_json_public()
    
    # Eliminar recurso
    @jwt_required()
    def delete(self, id):
        current_identity = get_jwt_identity()
        poem = db.session.query(PoemModel).get_or_404(id)
        claims = get_jwt()
        if claims['role'] == "admin" or current_identity == poem.user_id:
            db.session.delete(poem)
            db.session.commit()
            return '', 204
        else:
            return 'This user is not allowed to do that.', 403

    # Modificar recurso
    @jwt_required()
    def put(self, id):
        current_identity = get_jwt_identity()
        claims = get_jwt()
        if current_identity == poem.user_id:
            poem = db.session.query(PoemModel).get_or_404(id)
            data = request.get_json().items()
            for key, value in data:
                setattr(poem, key, value)
            db.session.add(poem)
            db.session.commit()
            return poem.to_json(), 201
        else:
            return 'This user is not allowed to do that.', 403


class Poems(Resource):
    # Obtener lista de poemas
    @jwt_required(optional=True)
    def get(self):
        current_identity = get_jwt_identity()
        page = 1
        perpage = 5
        if current_identity:
            poems = db.session.query(PoemModel).filter(PoemModel.user_id != current_identity).order_by(func.count(PoemModel.ratings))
        else:
            poems = db.session.query(PoemModel)
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
                    if key == "rating":
                        poems = poems.outerjoin(PoemModel.ratings).group_by(PoemModel.id).having(func.avg(RatingModel.score) == float(value))
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
                        # ordeno por nombre de autor
                        if value == "author_name":
                            poems = poems.order_by(PoemModel.user)
                        if value == "author_name[desc]":
                            poems = poems.order_by(PoemModel.user.desc())
        # hago el paginado de poemas pasandole la pagina y la cantidad de poemas por pagina, luego establezco un limite de poemas por pagina          
        poems = poems.paginate(page, perpage, True, 10)
        # retorno el to json short, el total de poemas y la pagina
        return jsonify({"poems":[poem.to_json_short() for poem in poems.items],
        "total": poems.total, "pages": poems.pages, "page": page})

    # Insertar recurso
    @jwt_required()
    def post(self):
        current_identity = get_jwt_identity()
        user = db.session.query(UserModel).get_or_404(current_identity)
        # Verificar si el usuario cumple con la condicion
        if len(user.poems) == 0 or (len(user.ratings))/(len(user.poems)) >= 5:
            # Obtener datos de la solicitud
            poem = PoemModel.from_json(request.get_json())
            poem.user_id = current_identity
            # Agrega el poema
            db.session.add(poem)
            db.session.commit()
            return poem.to_json(), 201
        else:
            return 'This user cannot add a poem. Need to add 5 Ratings first.', 403
