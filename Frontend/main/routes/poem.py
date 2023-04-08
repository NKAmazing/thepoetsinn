from http.client import ResponseNotReady
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, Response, make_response, flash
import requests
import json
from . import functions as f

poem = Blueprint('poem', __name__, url_prefix='/poem')


@poem.route('/read/poem/<int:id>')
def read_poem(id):
    poem = f.get_poem(id)
    poem = json.loads(poem.text)
    rating = f.get_ratings_by_poem_id(id)
    ratings = json.loads(rating.text)
    return render_template('read_poem.html', poem=poem, ratings=ratings)

@poem.route('/read/poem/rate/<int:id>', methods=['GET', 'POST'])
def read_poem_user(id):
    jwt = f.get_jwt()
    if jwt:
        # Obtener poemas
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        rating = f.get_ratings_by_poem_id(id)
        ratings = json.loads(rating.text)
        # Agregar un rating
        if request.method == 'POST':
            # obtengo el id del usuario
            user_id = f.get_id()
            score = request.form['score']
            commentary = request.form['commentary']
            rating = f.add_rating(user_id, id, score, commentary)
        
        return render_template('read_poem_user.html', poem=poem, ratings=ratings)
    else:
        return redirect(url_for("app.login"))
    
@poem.route('/create-poem', methods=['GET', 'POST'])
def create_poem():
    jwt = f.get_jwt()
    if (jwt):
        # Analizar si el usuario cumple con el requisito de tener mas de 5 ratings
        user_id = f.get_id()
        user_ratings = f.get_ratings_by_user_id(user_id)
        user_ratings = json.loads(user_ratings.text)
        print(user_ratings)
        if len(user_ratings) >= 5:
            
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
                return render_template('create_poem.html', jwt=jwt)
        else:
            flash('You need at least 5 ratings to create a poem.', 'error')
            return redirect(url_for('app.main_menu_user'))
    else:
        return redirect(url_for('app.login'))
    
@poem.route('/read/my-poem/<int:id>')
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

@poem.route('/my-poems')
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