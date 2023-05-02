from main import create_app
import os
from dotenv import load_dotenv



# Cargo las variables de entorno
load_dotenv()

# Llamo a la funcion que crea la aplicacion
app = create_app()

# Activo el contexto de la aplicacion
app.app_context().push()

if __name__ == '__main__':
    # Ejecuto la aplicacion con el modo debug activado
    app.run(debug = True, port = os.getenv("PORT"))

