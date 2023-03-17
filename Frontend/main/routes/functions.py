from flask import request, current_app
import requests, json

#--------------- Poems -----------------#

#Obtengo los poemas del poeta ayudandome del id del mismo.
def get_poems_by_id(id, page = 1, perpage = 3):
    api_url = f'{current_app.config["API_URL"]}/poems'
    # Envio de la pagina y cuantos datos por pagina.
    data = {"page": page, "perpage": perpage, "user_id": id}
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers(without_token = True)
    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)


#Obtengo un poema en especifico.
def get_poem(id):
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)


#Obtengo todos los poemas de la base de datos.
def get_poems(page=1, perpage=3):
    api_url = f'{current_app.config["API_URL"]}/poems'
    data = {"page": page, "perpage": perpage}
    headers = get_headers()
    return requests.get(api_url, json=data, headers=headers)

#--------------- Poems -----------------#


#--------------- User -----------------#

#Obtengo los datos del usuario.
def get_user_info(id):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    #Obtengo el jwt del logue e instancio el header y le agrego el jwt.
    headers = get_headers()

    #Creamos el response y le enviamos el data y headers
    return requests.get(api_url, headers=headers)


#Obtener un usuario en especifico.
def get_user(id):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)


#Obtengo el nombre del usuario
def get_username(user_id):
    headers = get_headers()
    api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
    response = requests.get(api_url, headers=headers)
    user = json.loads(response.text)
    return user["name"]

#--------------- User -----------------#


#--------------- Calificaciones -----------------#

#Obtener las calificaciones de un poema en especifico.
def get_ratings_by_poem_id(id):
    api_url = f'{current_app.config["API_URL"]}/ratings'

    data = {"poem_id": id}
    headers = get_headers()
    return requests.get(api_url, json = data, headers = headers)

#--------------- Calificaciones -----------------#


#--------------- Utilidades -----------------#

#Obtengo el json txt.
def json_load(response):
    return json.loads(response.text)


#Obtengo el email del usuario
def get_headers(without_token = False):
    jwt = get_jwt()
    if jwt and without_token == False:
        return {"Content-Type" : "application/json", "Authorization": f"Bearer {jwt}"}
    else:
        return {"Content-Type" : "application/json"}


#Obtener el token desde response.
def get_jwt():
    return request.cookies.get("access_token")


#Obtener el id desde response.
def get_id():
    return request.cookies.get("id")


#Hacer redirect

def redirect_to(url):
    return redirect(url_for(url))
#--------------- Utilidades -----------------#

#Editar un usuario.
def edit_user(id, name, email, password):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    data = {"id":id, "name": name, "email": email, "passw": password}
    headers = get_headers()
    return requests.put(api_url, json = data, headers = headers)