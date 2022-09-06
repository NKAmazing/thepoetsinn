from flask import Flask, Blueprint, render_template, request, redirect, url_for, Response



app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/read/poem')
def read_poem():
    return render_template('read_poem.html')

@app.route('/login')
def login():
    return render_template('login.html')

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