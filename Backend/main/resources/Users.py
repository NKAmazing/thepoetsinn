# Archivo para el recurso usuarios

from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
from main.models import PoemModel
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.auth import decorators


# Utilizo una clase Resources como recurso
class User(Resource):
    
    # Obtengo recurso
    @jwt_required(optional=True)
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        #Obtener claims de adentro del JWT
        claims = get_jwt()
        # Verifica si logeo un usuario
        if 'role' in claims:
            # Verifica que el rol sea admin
            if claims['role'] == "admin":
                return user.to_json_admin()
            # Verifica que el rol sea user
            elif claims['role'] == "user":
                return user.to_json()
        # Si no logea nadie, muestra to json public
        else:
            return user.to_json_public()
    
    # Eliminar recurso
    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        user_id = int(user_id)
        id = int(id)
        user = db.session.query(UserModel).get_or_404(id)
        claims = get_jwt()
        if claims['role'] == "admin" or user_id == id:
            db.session.delete(user)
            db.session.commit()
            return '', 204
        else:
            return 'This user is not allowed to do that.', 403

    # Modificar recurso
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()
        claims = get_jwt()
        id = int(id)
        print(user_id, id)
        if claims['role'] == "admin" or user_id == id:
            user = db.session.query(UserModel).get_or_404(id)
            data = request.get_json().items()
            for key, value in data:
                setattr(user, key, value)
            db.session.add(user)
            db.session.commit()
            return user.to_json_short(), 201
        else:
            return 'This user is not allowed to do that.', 403


class Users(Resource):
    
    # Obtener lista de usuarios
    @admin_required
    def get(self):
        # users = db.session.query(UserModel).all()
        users = db.session.query(UserModel)
        page = 1
        perpage = 5
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                # itero con un if, todos los filtros correspondientes
                if key == "page":
                    page = int(value)
                if key == "perpage":
                    perpage = int(value)
                if key == "id":
                    users = users.filter(UserModel.id == value)
                if key == "username":
                    users = users.filter(UserModel.username.like("%" + value + "%"))
                # agrego el sort by
                if key == "sort_by":
                    # ordeno por cantidad de poemas
                    if value == "poems":
                        # utilizo un outerjoin y luego un group by para obtener las calificaciones del poema, luego hago un promedio
                        users = users.outerjoin(UserModel.poems).group_by(UserModel.id).order_by(func.count(PoemModel.id))
                    if value == "poems[desc]":
                        # misma operacion pero ahora en modo descendente
                        users = users.outerjoin(UserModel.poems).group_by(UserModel.id).order_by(func.count(PoemModel.id).desc())
                    # ordenamiento por nombre
                    if value == "name":
                        users = users.order_by(UserModel.username)
                    # ordenamiento por nombre descendente
                    if value == "name[desc]":
                        users = users.order_by(UserModel.username.desc())
        # hago el paginado de poemas pasandole la pagina y la cantidad de poemas por pagina, luego establezco un limite de poemas por pagina          
        users = users.paginate(page, perpage, True, 10)
        # retorno el to json short, el total de poemas y la pagina
        return jsonify({"users":[user.to_json_short() for user in users.items],
        "total": users.total, "pages": users.pages, "page": page})

    # Insertar recurso
    @admin_required
    def post(self):
        # Obtener datos de la solicitud
        user = UserModel.from_json(request.get_json())
        print(user)
        db.session.add(user)
        db.session.commit()
        print(user)
        return user.to_json(), 201
