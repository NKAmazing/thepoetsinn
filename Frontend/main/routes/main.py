from http.client import ResponseNotReady
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, Response, make_response, flash
import requests
import json
from . import functions as f
from flask_paginate import Pagination, get_page_parameter
from math import ceil


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/register', methods=["GET", "POST"])
def register():
    if (request.method == "POST"):
        # Obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs.
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = "user"

        if username != None and email != None and password != None:
            # Hago el registro.
            response = f.register(username, email, password, role)
            if (response.ok):
                # Muestro mensaje de exito.
                flash("Registered user successfully!", "success")
                # Redirecciono al login.
                return redirect(url_for("app.login"))
        else:
            # Muestro mensaje de error.
            flash("You must complete all the data fields to be able to register.", "error")
            # Redirecciono al registro.
            return render_template("register.html", error="Error registering user. Data incomplete.")
    else:
        return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        # Obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs.
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email != None and password != None:
            # Hago el login.
            response = f.login(email, password)
            if (response.ok):
                # Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]
                # Obtengo el id del usuario.
                user_id = str(response["id"])
                # Obtengo la informacion del usuario.
                user = f.get_user(user_id)
                # Obtengo el usuario en formato json.
                user = json.loads(user.text)
                # Hago el response redireccionando al main menu.
                resp = make_response(redirect(url_for("app.main_menu_user")))
                # Seteo el token en el response.
                resp.set_cookie("access_token", token)
                # Seteo el id en el response.
                resp.set_cookie("id", user_id)
                
                return resp
            
        return render_template("login.html", error="Wrong user or password")
    else:
        return render_template("login.html")
    
@app.route('/logout')
def logout():
    # Redirecciono al login.
    resp = make_response(redirect('login'))
    # Elimino el token.
    resp.set_cookie('access_token', '', expires=0)
    return resp

@app.route('/')
def main_menu():

     # Obtener valores del formulario en html
    filter_title = request.form.get("filter_title")
    filter_author = request.form.get("filter_author")
    filter_rating = request.form.get("filter_rating")

 # Paginacion
    try:
        page = int(request.form.get("_page"))
    except:
        page = request.form.get("_page")
        if (page == "< Atras"):
            page = int(f.get_poems_page()) - 1
        elif (page == "Siguiente >"):
            page = int(f.get_poems_page()) + 1
        else:
            page = f.get_poems_page()
            if (page == None):
                page = 1
            else:
                page = int(page)

    if(request.method == "POST" and (filter_title != "" or filter_author != "" or filter_rating != None)):
        # Obtener los poemas.
        response = f.get_poems_by_filters(title= filter_title, author= filter_author, rating= filter_rating, page = page)
    else:
        # Obtener los poemas
        response = f.get_poems(page=page)
        poems = f.get_json(response)
        list_poems = poems["poems"]
        # Redireccionar a función de vista
        response = make_response(render_template('main_menu.html', poems = list_poems, page = int(page)))
    response.set_cookie("poems_page", str(page))
    return response

# @app.route('/home')
# def main_menu_user():
#     jwt = f.get_jwt()
#     if jwt:
#         # Hago la petición a la API para obtener los poemas.
#         response = f.get_poems()
#         # Obtener poemas en json
#         poems = json.loads(response.text)
#         # Obtener lista de poemas
#         list_poems = poems["poems"]
        
#         return render_template('main_menu_user.html', poems=list_poems)
#     else:
#         return redirect(url_for("app.login"))

@app.route('/home')
def main_menu_user():
    # Obtener el número de página actual y la cantidad de elementos por página
    page = int(request.args.get('page', 1))
    per_page = 6  # Cambia esto a la cantidad de elementos que deseas mostrar por página

    jwt = f.get_jwt()
    if jwt:
        # Hago la petición a la API para obtener los poemas.
        response = f.get_poems(page=page, perpage=per_page)
        # Obtener poemas en json
        poems = json.loads(response.text)
        # Obtener lista de poemas
        list_poems = poems["poems"]

        # # Calcular el número de páginas
        # total_pages = f.get_total_pages(page=page, per_page=per_page)
        # print("Esto es total pages: ", total_pages)

        # Calcular el rango de elementos a mostrar en la página actual
        start = (page - 1) * per_page
        end = start + per_page
        # poems_paginated = list_poems[start:end]
        # print(poems_paginated)

        return render_template('main_menu_user.html', poems=list_poems, page=page)
    else:
        return redirect(url_for("app.login"))





