import os
from flask import Flask
from dotenv import load_dotenv
from main.routes import main, poem, user

def create_app():

    app = Flask(__name__)

    load_dotenv()

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config["API_URL"] = os.getenv("API_URL")

    

    app.register_blueprint(main.app)
    app.register_blueprint(user.user)
    app.register_blueprint(poem.poem)

    return app