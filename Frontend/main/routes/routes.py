from flask import Flask, Blueprint, render_template, request, redirect, url_for, Response



app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/read-poem')
def read_poem():
    return render_template('read_poem.html')

@app.route('/login')
def login():
    return render_template('login.html')