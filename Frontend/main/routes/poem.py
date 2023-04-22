from http.client import ResponseNotReady
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, Response, make_response, flash
import requests
import json
from . import functions as f

poem = Blueprint('poem', __name__, url_prefix='/poem')


@poem.route('/read/poem/<int:id>')
def read_poem(id):
    # Obtener poema
    poem = f.get_poem(id)
    poem = json.loads(poem.text)

    # Obtener ratings
    rating = f.get_ratings_by_poem_id(id)
    ratings = json.loads(rating.text)

    return render_template('read_poem.html', poem=poem, ratings=ratings)

@poem.route('/read/poem/rate/<int:id>', methods=['GET', 'POST'])
def read_poem_user(id):
    jwt = f.get_jwt()
    if jwt:
        # Obtener poema
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        rating = f.get_ratings_by_poem_id(id)
        ratings = json.loads(rating.text)

        # Agregar un rating
        if request.method == 'POST':
            # Obtengo el id del usuario
            user_id = f.get_id()

            # Obtengo el score y el comentario
            score = request.form['score']
            commentary = request.form['commentary']

            # Agrego el rating
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
        if len(user_ratings) >= 5:
            
            if (request.method == "POST"):
                # Obtengo el titulo y el body del poema
                title = request.form.get("title")
                body = request.form.get("body")

                if title != "" and body != "":
                    # Agrego el poema
                    response = f.add_poem(user_id, title, body)
                    if response.ok:
                        response = f.json_load(response)
                        flash('Poem created successfully.', 'success')
                        return redirect(url_for('poem.read_poem_user', id=response["id"], jwt=jwt))
                    else:
                        # Muestro un error y redirijo al usuario a la pagina de creacion de poemas
                        flash('Something went wrong.', 'error')
                        return redirect(url_for('poem.create_poem'))
                else:
                        flash('Error creating poem. You must fill all the fields before creating a poem.', 'error')
                        return redirect(url_for('poem.create_poem'))
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
    
# Editar poemas
@poem.route('/edit-poem/<int:id>', methods=['GET', 'POST'])
def edit_poem(id):
    jwt = f.get_jwt()
    if (jwt):
        # Obtener los datos del poema
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        if (request.method == "POST"):
            # Obtener los datos del formulario
            title = request.form.get("title")
            body = request.form.get("body")
            # Verifico que no esten vacios
            if title != "" and body != "":
                # Hago el request
                response = f.edit_poem(id, title, body)
                # Verifico que el request haya sido exitoso
                if response.ok:
                    return make_response(redirect(url_for('poem.read_my_poem', id=id)))
                else:
                    return redirect(url_for('poem.edit_poem', id=id))
            else:
                return redirect(url_for('poem.edit_poem', id=id))
        else:
            return render_template('edit_poem.html', jwt=jwt, poem=poem)
    else:
        return redirect(url_for('app.login'))
    
# Eliminar poemas
@poem.route('/delete-poem/<int:id>')
def delete_poem(id):
    jwt = f.get_jwt()
    if jwt:
        response = f.delete_poem(id)
        if response.ok:
            flash('Poem successfully deleted.', 'success')
            return redirect(url_for('poem.my_poems'))
        else:
            flash('Something went wrong.', 'error')
            return redirect(url_for('poem.my_poems'))
    else:
        return redirect(url_for('app.login'))