# Archivo principal de la aplicacion

from main import create_app
import os
from main import db

# Llamo a la funcion que crea la aplicacion
app = create_app()


# Activo el contexto de la aplicacion
app.app_context().push()

if __name__ == '__main__':
    # Creo la base de datos
    db.create_all()
    # Ejecuto la aplicacion con el modo debug activado
    app.run(debug = True, port = os.getenv("PORT"))