from os import access
from flask import request, jsonify, Blueprint
from .. import db
from main.models import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

# Blueprint para acceder a los metodos de autenticacion
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Metodo de logeo
@auth.route('/login', methods=['POST'])
def login():
    # Busca al usuario en la db por mail
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first_or_404()
    # Valida la contraseña
    if user.validate_pass(request.get_json().get("password")):
        # Genera un nuevo token
        # Pasa el objeto user como identidad
        access_token = create_access_token(identity = user)
        # Devolver valores y token
        data = {
            'id': user.id,
            'email': user.email,
            'access_token': access_token
        }

        return data, 200
    else:
        return 'Incorrect password', 401
    

# Metodo de registro
@auth.route('/register', methods=['POST'])
def register():
    # Obtener usuario
    user = UserModel.from_json(request.get_json())
    # Verificar si el mail ya existe en la base de datos
    exists = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
    # Si existe el email, retorna error de email duplicado
    if exists:
        return 'Duplicated email', 409
    else:
        try:
            # Agregar user a base de datos
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            # En caso de fallar, cancelar y devolver error.
            db.session.rollback()
            return str(error), 409
        return user.to_json() , 201