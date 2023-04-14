from http.client import ResponseNotReady
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, Response, make_response, flash
import requests
import json
from . import functions as f

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/login', methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        # Obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs.
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email != None and password != None:

            api_url = f'{current_app.config["API_URL"]}/auth/login'
            # Envio de logueo
            data = {"email": email, "password":password}
            headers = {"Content-Type" : "application/json"}

            response = requests.post(api_url, json=data, headers=headers)

            print(response.text)

            if (response.ok):
                # Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])

                response = f.get_poems()

                poems = json.loads(response.text)

                list_poems = poems["poems"]
                user = f.get_user(user_id)
                user = json.loads(user.text)

                # resp = make_response(render_template("main_menu_user.html", poems=list_poems, user=user, jwt=token))
                resp = make_response(redirect(url_for("app.main_menu_user")))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                
                return resp
            
        return render_template("login.html", error="Wrong user or password")
    else:
        return render_template("login.html")
    
@app.route('/logout')
def logout():
    resp = make_response(redirect('login'))
    resp.set_cookie('access_token', '', expires=0)
    return resp

@app.route('/')
def main_menu():
    # Paginacion
    try:
        page = int(request.form.get('n_page'))
    except:
        page = request.form.get("n_page")
        if (page == "< Back"):
            page = int(f.get_poems_page()) - 1
        elif (page == "Next >"):
            page = int(f.get_poems_page()) + 1
        else:
            page = f.get_poems_page()
            if (page == None):
                page = 1
            else:
                page = int(page)
    # Obtener los poemas
    response = f.get_poems(page=page)
    poems = f.get_json(response)
    list_poems = poems["poems"]
    # Redireccionar a función de vista
    response = make_response(render_template('main_menu.html', poems = list_poems, page = int(page)))
    response.set_cookie("poems_page", str(page))
    return response

@app.route('/home')
def main_menu_user():
    if request.cookies.get("access_token"):
        api_url = "http://127.0.0.1:8500/poems"
        data = {"page": 1,"perpage": 12}
        jwt = request.cookies.get("access_token")
        print(jwt)
        headers = {"Content-Type": "application/json", "Authorization": "BEARER {}".format(jwt)}
        response = requests.get(api_url, json=data, headers=headers)
        print(response.status_code)

        # obtener lista de poemas en json
        poems = json.loads(response.text)
        # print(poems)

        list_poems = poems["poems"]
        # print(list_poems)
        for poem in list_poems:
            print(poem)  
        print(type(list_poems))

        return render_template('main_menu_user.html', poems=list_poems)
    else:
        return redirect(url_for("app.login"))