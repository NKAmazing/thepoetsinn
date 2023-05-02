from http.client import ResponseNotReady
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, Response, make_response, flash
import requests
import json
from . import functions as f
from flask_paginate import Pagination, get_page_parameter
from math import ceil

# Creo el blueprint
app = Blueprint('app', __name__, url_prefix='/')

# Registro de usuario
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

# Login de usuario
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

# Logout de usuario
@app.route('/logout')
def logout():
    # Redirecciono al login.
    resp = make_response(redirect('login'))
    # Elimino el token.
    resp.set_cookie('access_token', '', expires=0)
    return resp

# Main menu publico
@app.route('/', methods=['GET', 'POST'])
def main_menu():
    # Obtener el número de página actual y la cantidad de elementos por página
    page = int(request.args.get('page', 1))
    per_page = 6  # Cambiar esto a la cantidad de elementos que deseas mostrar por página
    
    # Obtener los poemas
    response = f.get_poems(page=page, perpage=per_page)
    poems = f.get_json(response)
    list_poems = poems["poems"]

    # Calcular el numero de poemas
    total_poems = f.count_poems()
    # Convierto su valor a int
    total_poems = int(total_poems.text)

    # Calcular el numero de paginas
    total_pages = ceil(total_poems / per_page)
    
    # Definir opciones de filtro
    filter_options = ['Username', 'User ID', 'Rating', 'Title', 'Datetime [gte]', 'Datetime [lte]']

    # Definir opciones de ordenamiento
    sort_options = ['Datetime [Asc]', 'Datetime [Desc]', 'Rating [Asc]', 'Rating [Desc]', 'Author [Asc]', 'Author [Desc]']

    # Obtener el valor de la opcion de filtro ingresado por el usuario
    filter_option = request.args.get("filter_option")

    # Obtener el valor de la opcion de ordenamiento ingresado por el usuario
    sort_option = request.args.get("sort_option")

    print("sort_option: ", sort_option)

    if sort_option != None:

        # Asigno un valor mas grande de perpage
        per_page = 1000

        response = f.get_poems_by_sort(sort_option=sort_option, page=page, perpage=per_page)
        poems = f.get_json(response)
        list_poems = poems["poems"]

        total_poems = len(list_poems)

        # Calcular el numero de paginas
        total_pages = ceil(total_poems / per_page)

        response = make_response(render_template('main_menu.html', poems = list_poems, page = page, total_pages=total_pages, filter_options=filter_options, sort_option=sort_option, sort_options=sort_options))
        return response

    # Si el usuario eligio una opcion de filtro
    if request.method == "POST":

        # Asigno un valor mas grande de perpage
        per_page = 1000

        # Obtener el valor de la opcion de filtro ingresado por el usuario
        filter_value = request.form.get("filter_value")

        response = f.get_poems_by_filters(filter_option=filter_option, filter_value=filter_value, page=page, perpage=per_page)
        poems = f.get_json(response)
        list_poems = poems["poems"]

        total_poems = len(list_poems)

        # Calcular el numero de paginas
        total_pages = ceil(total_poems / per_page)

        response = make_response(render_template('main_menu.html', poems = list_poems, page = page, total_pages=total_pages, filter_option=filter_option, filter_value=filter_value, filter_options=filter_options))
        return response


    # Redireccionar a función de vista
    response = make_response(render_template('main_menu.html', poems = list_poems, page = page, total_pages=total_pages, filter_options=filter_options, filter_option=filter_option, sort_options=sort_options))
    return response

# Main menu de usuario
@app.route('/home')
def main_menu_user():
    # Obtener el número de página actual y la cantidad de elementos por página
    page = int(request.args.get('page', 1))
    per_page = 6  # Cambiar esto a la cantidad de elementos que deseas mostrar por página

    jwt = f.get_jwt()
    if jwt:
        # Hago la petición a la API para obtener los poemas.
        response = f.get_poems(page=page, perpage=per_page)
        # Obtener poemas en json
        poems = json.loads(response.text)
        # Obtener lista de poemas
        list_poems = poems["poems"]

        # Calcular el numero de poemas
        total_poems = f.count_poems()
        # Convierto su valor a int
        total_poems = int(total_poems.text)

        # Calcular el numero de paginas
        total_pages = ceil(total_poems / per_page)

        return render_template('main_menu_user.html', poems=list_poems, page=page, total_pages=total_pages)
    else:
        return redirect(url_for("app.login"))





