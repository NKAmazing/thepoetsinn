from flask import Flask, Blueprint, render_template, request, redirect, url_for, Response, make_response
import requests
import json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/read/poem')
def read_poem():
    return render_template('read_poem.html')

@app.route('/login')
def login():
    api_url = "http://127.0.0.1:8500/auth/login"
    
    data = {"email": "teirione@hotmail.com", "password": "tatizapata"}

    headers = {"Content-Type": "application/json"}

    response = requests.post(api_url, json = data, headers = headers)

    print(response.status_code)
    print(response.text)

    # Obtener el token desde response
    token = json.loads(response.text)
    token = token["access_token"]
    print(token)

    # Guardar el token en las cookies y devuelve la pagina
    resp = make_response(render_template("login.html"))
    resp.set_cookie("access_token", token)

    return resp

    # return render_template('login.html')

@app.route('/home')
def main_menu_user():
    return render_template('main_menu_user.html')

@app.route('/read/poem/rate')
def read_poem_user():
    return render_template('read_poem_user.html')

@app.route('/my-profile')
def profile():
    return render_template('profile.html')

@app.route('/edit-profile')
def edit_user():
    return render_template('edit_user.html')

@app.route('/create-poem')
def create_poem():
    return render_template('create_poem.html')

@app.route('/read/my-poem')
def read_my_poem():
    return render_template('read_my_poem.html')

@app.route('/my-poems')
def my_poems():
    return render_template('my_poems.html')