from http.client import ResponseNotReady
from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, Response, make_response, flash
import requests
import json
from . import functions as f

# Creo el blueprint
user = Blueprint('user', __name__, url_prefix='/user')

# Ver mi perfil de usuario
@user.route('/my-profile', methods=['GET', 'POST'])
def profile():
    jwt = f.get_jwt()
    if jwt:
        id = f.get_id()
        # Cargo la informacion del usuario
        user = f.get_user_info(id)
        user = json.loads(user.text)
        return render_template('profile.html', jwt=jwt, user = user)
    else:
        return redirect(url_for('app.login'))

# Editar nombre de usuario
@user.route('/edit_username', methods=['GET', 'POST'])
def edit_username():
    jwt = f.get_jwt()
    if jwt:
        # Obtengo el id del usuario
        user_id = f.get_id()
        # Obtengo la informacion del usuario
        user_info = f.get_user_info(user_id)
        if request.method == 'POST':
            # Obtengo el nuevo username
            new_username = request.form['username']
            if new_username != "":
                # Actualizo el username
                response = f.edit_username(user_id, new_username)
                if response.ok:
                    flash('Username successfully updated!', 'success')
                    print("Username successfully updated!")
                    return redirect(url_for('user.profile'))
                else:
                    flash('Failed to update username.', 'error')
            else:
                flash('Please enter a username.', 'error')
                return redirect(url_for('user.edit_username'))
        else:
            return render_template('edit_username.html', user=user_info)
    else:
        return redirect(url_for('app.login'))

# Editar email 
@user.route('/edit-email', methods=['GET', 'POST'])
def edit_email():
    jwt = f.get_jwt()
    if jwt:
        # Obtengo el id del usuario
        user_id = f.get_id()
        # Obtengo la informacion del usuario
        user_info = f.get_user_info(user_id)
        if request.method == 'POST':
            # Obtengo el nuevo email
            new_email = request.form['email']
            if new_email != "":
                # Actualizo el email
                response = f.edit_email(user_id, new_email)
                if response.ok:
                    flash('Email successfully updated!', 'success')
                    print("Email successfully updated!")
                    return redirect(url_for('user.profile'))
                else:
                    flash('Failed to update email.', 'error')
            else:
                flash('Please enter an email.', 'error')
                return redirect(url_for('user.edit_email'))
        else:
            return render_template('edit_user_email.html', user=user_info)
    else:
        return redirect(url_for('app.login'))

# Editar contraseña    
@user.route('/edit-password', methods=['GET', 'POST'])
def edit_password():
    jwt = f.get_jwt()
    if jwt:
        # Obtengo el id del usuario
        user_id = f.get_id()
        # Obtengo la informacion del usuario
        user_info = f.get_user_info(user_id)
        if request.method == 'POST':
            # Obtengo la nueva contraseña
            new_password = request.form['password']
            if new_password != "":
                # Actualizo la contraseña
                response = f.edit_password(user_id, new_password)
                print(new_password)
                if response.ok:
                    flash('Password successfully updated!', 'success')
                    print("Password successfully updated!")
                    return redirect(url_for('user.profile'))
                else:
                    flash('Failed to update password.', 'error')
            else:
                flash('Please enter a password.', 'error')
                return redirect(url_for('user.edit_password'))
        else:
            return render_template('edit_user_password.html', user=user_info)
    else:
        return redirect(url_for('app.login'))
    
# Eliminar cuenta
@user.route('/delete-account/<int:id>')
def delete_user(id):
    jwt = f.get_jwt()
    # Verifico que el usuario este logueado
    if jwt:
        # Borro el usuario
        response = f.delete_user(id)
        # Verifico que se haya borrado correctamente
        if response.ok:
            flash('Account successfully deleted!', 'success')
            return redirect(url_for('app.login'))
        else:
            flash('Failed to delete account.', 'error')
            return redirect(url_for('user.profile'))
    else:
        return redirect(url_for('app.login'))