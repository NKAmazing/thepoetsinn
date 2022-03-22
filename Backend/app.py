import os
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT'))

# Comentario
