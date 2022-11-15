import email
from http.client import ResponseNotReady
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, Response, make_response
import requests
import json
from . import functions as f


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/read/poem')
def read_poem():
    return render_template('read_poem.html')

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

@app.route('/read/poem/rate/<int:id>')
def read_poem_user(id):
    poem = f.get_poem(id)
    poem = json.loads(poem.text)
    rating = f.get_ratings_by_poem_id(id)
    rating = json.loads(rating.text)
    print(rating)
    print(type(rating))
    return render_template('read_poem_user.html', poem=poem, rating=rating)

@app.route('/my-profile')
def profile():
    if request.cookies.get('access_token'):
        jwt = f.get_jwt()
        id = f.get_id()
        user = f.get_user_info(id)
        user = json.loads(user.text)
        print(user)
        return render_template('profile.html', jwt=jwt, user = user)
    else:
        return redirect('app.login')

@app.route('/edit-profile')
def edit_user():
    id = f.get_id()
    user = f.get_user(id)
    user = json.loads(user.text)
    return render_template('edit_user.html', user=user)

@app.route('/create-poem', methods=['GET', 'POST'])
def create_poem():
    jwt = f.get_jwt()
    if (jwt):
        if (request.method == "POST"):
        
            title = request.form.get("title")
            body = request.form.get("body")

            id = f.get_id()

            data = {"user_id": id, "title": title, "body": body}
            headers = f.get_headers(without_token=False)

            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)

                if response.ok:
                    response = f.json_load(response)
                    return redirect(url_for('app.read_poem_user', id=response["id"], jwt=jwt))
                else:
                    return redirect(url_for('app.create_poem'))
            else:
                    return redirect(url_for('app.create_poem'))
        else:
            return render_template('create_poem.html', jwt=f.get_jwt())
    else:
        return redirect(url_for('app.login'))

@app.route('/read/my-poem/<int:id>')
def read_my_poem(id):
    if request.cookies.get('access_token'):
        jwt = f.get_jwt()
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        resp = f.get_ratings_by_poem_id(id)
        ratings = json.loads(resp.text)
        return render_template('read_my_poem.html', jwt=jwt, poem=poem, ratings=ratings)
    else:
        return redirect(url_for('app.login'))

@app.route('/my-poems')
def my_poems():
    if request.cookies.get('access_token'):
        jwt = f.get_jwt()
        id = f.get_id()
        resp = f.get_poems_by_id(id)
        poems = json.loads(resp.text)
        poems_list = poems["poems"]
        return render_template('my_poems.html', jwt=jwt, poems = poems_list)
    else:
        return redirect(url_for('app.login'))

@app.route('/logout')
def logout():
    resp = make_response(redirect('login'))
    resp.set_cookie('access_token', '', expires=0)
    return resp