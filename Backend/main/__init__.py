import os
from flask import Flask
from dotenv import load_dotenv

# importar libreria flask_restful
from flask_restful import Api

# importar sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# importar Flask JWT
from flask_jwt_extended import JWTManager

# Inicializar API de Flask Restful
api = Api()

# Inicializar SQLAlchemy
db = SQLAlchemy()

# Inicializar JWT
jwt = JWTManager()

def create_app():

    app = Flask(__name__)

    load_dotenv()

    #Si no existe el archivo de base de datos crearlo (solo valido si se utiliza SQLite)
    if not os.path.exists(os.getenv('DB_PATH')+os.getenv('DB_NAME')):
        os.mknod(os.getenv('DB_PATH')+os.getenv('DB_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Url de configuracion de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DB_PATH')+os.getenv('DB_NAME')
    db.init_app(app)

    # importar directorio de recursos
    import main.resources as resources

    # Cargar a la API el recurso Poem e indicar ruta
    api.add_resource(resources.PoemResource, '/poem/<id>')

    # Cargar a la API el recurso Poems e indicar ruta
    api.add_resource(resources.PoemsResource, '/poems')

    # Cargar a la API el recurso User e indicar ruta
    api.add_resource(resources.UserResource, '/user/<id>')

    # Cargar a la API el recurso Users e indicar ruta
    api.add_resource(resources.UsersResource, '/users')

    # Cargar a la API el recurso Punctuation e indicar ruta
    api.add_resource(resources.RatingResource, '/rating/<id>')

    # Cargar a la API el recurso Punctuations e indicar ruta
    api.add_resource(resources.RatingsResource, '/ratings')

    #Cargar la aplicacion en la API de Flask Restful
    api.init_app(app)
    
    # Cargar clave secreta
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    #Cargar tiempo de expiracion de los tokens
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    from main.auth import routes
    # Importar bluesprint
    app.register_blueprint(auth.routes.auth)

    return app