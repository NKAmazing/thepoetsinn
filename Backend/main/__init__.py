import os
from flask import Flask
from dotenv import load_dotenv
# importar libreria flask_restful
from flask_restful import Api
# importar directorio de recursos
import main.resources as resources

# Inicializar API de Flask Restful

api = Api()

def create_app():

    app = Flask(__name__)

    load_dotenv()

    # Cargar a la API el recurso Poem e indicar ruta
    api.add_resource(resources.PoemResource, '/poem/<id>')

    # Cargar a la API el recurso Poems e indicar ruta
    api.add_resource(resources.PoemsResource, '/poems')

    # Cargar a la API el recurso User e indicar ruta
    api.add_resource(resources.UserResource, '/user/<id>')

    # Cargar a la API el recurso Users e indicar ruta
    api.add_resource(resources.UsersResource, '/users')

    # Cargar a la API el recurso Punctuation e indicar ruta
    api.add_resource(resources.PunctuationResource, '/punctuation/<id>')

    # Cargar a la API el recurso Punctuations e indicar ruta
    api.add_resource(resources.PunctuationsResource, '/punctuations')

    #Cargar la aplicación en la API de Flask Restful
    api.init_app(app)
    
    return app