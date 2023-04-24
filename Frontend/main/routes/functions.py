from flask import request, current_app
import requests, json

#--------------- Poems -----------------#

#Obtengo los poemas del poeta ayudandome del id del mismo.
def get_poems_by_id(id, page = 1, perpage = 10):
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
def get_poems(jwt = None, page = 1, perpage = 6):
    api_url = f'{current_app.config["API_URL"]}/poems'
    data = {"page": page, "perpage": perpage}
    if jwt:
        headers = get_headers(jwt = jwt)
    else:
        headers = get_headers(without_token = True)
    return requests.get(api_url, json = data, headers = headers)

def get_poems_by_filters(title = "", author = "", rating = None, page = 1, perpage = 3):
    api_url = f'{current_app.config["API_URL"]}/poems'
    # Envio de la pagina y cuantos datos por pagina.

    if (title == None):
        title = ""
    if (author == None):
        author = ""
    if (rating == None):
        data = {"page": page, "perpage": perpage, "title": title, "username": author}
    else:
        data = {"page": page, "perpage": perpage, "title": title, "username": author, "rating": int(rating)}

    # Para obtener filtros, solo se puede en usuarios sin token.
    headers = get_headers(without_token = True)

    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)


# Obtener la pagina de los poemas.
def get_poems_page():
    return request.cookies.get("poems_page")

# Agregar un poema.
def add_poem(user_id, title, body):
    api_url = f'{current_app.config["API_URL"]}/poems'
    data = {"user_id": user_id, "title": title, "body": body}
    headers = get_headers(without_token = False)
    return requests.post(api_url, json = data, headers = headers)

# Editar un poema en especifico.
def edit_poem(id, title, body):
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    data = {"title": title, "body": body}
    headers = get_headers()
    return requests.put(api_url, json = data, headers = headers)

# Eliminar un poema en especifico.
def delete_poem(id):
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    headers = get_headers(without_token=False)
    return requests.delete(api_url, headers=headers)


#--------------- Poems -----------------#


#--------------- User -----------------#

# Obtengo los datos del usuario.
def get_user_info(id):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    #Obtengo el jwt del logue e instancio el header y le agrego el jwt.
    headers = get_headers()

    #Creamos el response y le enviamos el data y headers
    return requests.get(api_url, headers=headers)


# Obtener un usuario en especifico.
def get_user(id):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)


# Obtengo el nombre del usuario
def get_username(user_id):
    headers = get_headers()
    api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
    response = requests.get(api_url, headers=headers)
    user = json.loads(response.text)
    return user["name"]

# Borrar cuenta de usuario.
def delete_user(id):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    headers = get_headers(without_token=False)
    return requests.delete(api_url, headers=headers)

#--------------- User -----------------#


#--------------- Calificaciones -----------------#

#Obtener las calificaciones de un poema en especifico.
def get_ratings_by_poem_id(id):
    api_url = f'{current_app.config["API_URL"]}/ratings'

    data = {"poem_id": id}
    headers = get_headers()
    return requests.get(api_url, json = data, headers = headers)

#--------------- Calificaciones -----------------#

def get_ratings_by_user_id(id):
    api_url = f'{current_app.config["API_URL"]}/ratings'

    data = {"user_id": id}
    headers = get_headers()
    return requests.get(api_url, json = data, headers = headers)


#Agregar una calificacion a un poema.
def add_rating(user_id, poem_id, score, commentary):
    api_url = f'{current_app.config["API_URL"]}/ratings'
    data = {"user_id": user_id, "poem_id": poem_id, "score": score, "commentary": commentary}
    headers = get_headers(without_token=False)
    return requests.post(api_url, json = data, headers = headers)

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
def edit_user(id, username, email, password):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    data = {"id":id, "username": username, "email": email, "passw": password}
    headers = get_headers()
    return requests.put(api_url, json = data, headers = headers)

# Editar un nombre de usuario.
def edit_username(id, username):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    data = {"id":id, "username": username}
    headers = get_headers()
    return requests.put(api_url, json = data, headers = headers)

# Editar un email de usuario.
def edit_email(id, email):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    data = {"id":id, "email": email}
    headers = get_headers()
    return requests.put(api_url, json = data, headers = headers)

# Editar un password de usuario.
def edit_password(id, password):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    data = {"id":id, "password": password}
    headers = get_headers()
    return requests.put(api_url, json = data, headers = headers)

def get_json(resp):
    return json.loads(resp.text)

# Registrar un usuario.
def register(username, email, password, role):
    api_url = f'{current_app.config["API_URL"]}/auth/register'

    # Envio de logueo.
    data = {"username": username, "email": email, "password": password, "role": role}
    headers = get_headers(without_token = True)

    # Generamos la respuesta, mandando endpoint, data diccionario, y el headers que es el formato como aplication json.
    return requests.post(api_url, json = data, headers = headers)

# Loguear un usuario.
def login(email, password):
    api_url = f'{current_app.config["API_URL"]}/auth/login'
    # Envio de logueo
    data = {"email": email, "password":password}
    headers = {"Content-Type" : "application/json"}
    # Generamos la respuesta, mandando endpoint, data diccionario, y el headers que es el formato como aplication json.
    return requests.post(api_url, json=data, headers=headers)