# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import yagmail as yagmail
import string
import random
from apps.authentication.util import hash_pass
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)


from apps import db, login_manager

from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, ForgotPass
from apps.authentication.models import Empleado

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if 'login' in request.form:
        # read form data
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        # Locate user
        user = Empleado.query.filter_by(username=username).first()

        # Check the password
        print(user)
        if user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))
        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    print(current_user.role)
    if current_user.role == 'Admin':
        return redirect(url_for('home_blueprint.usuariosAll'))
    else:
        return redirect(url_for('home_blueprint.info_empleado'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Empleado.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Empleado.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Empleado(**request.form)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        if current_user.role == 'Admin':
            return redirect(url_for('home_blueprint.dashboard'))
        else:
            return redirect(url_for('home_blueprint.info_empleado'))

    else:
        return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/forgot', methods=['GET', 'POST'])
def forgot():
    forgotpass= ForgotPass(request.form)
    if 'forgot' in request.form:
        email = request.form['email']
        user = Empleado.query.filter_by(email=email).first()
        
        print(user)
        if user:
            length_of_string = 8
            new= ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
            value= hash_pass(new)
            user.password = value
            db.session.commit()
            yag = yagmail.SMTP('componentepractico9@gmail.com', '1810Uninorte')
            yag.send(to= email, subject='Recuperacion de cuenta', contents='nombre de cuenta: '+user.username+'\n'+'contraseña nueva: '+new)
            return render_template('accounts/olividar_contraseña.html',
                               msg='Cuenta enviada a tu correo electronico',
                               form=forgotpass)
        
        else:
         return render_template('accounts/olividar_contraseña.html',
                               msg='Wrong Email user',
                               form=forgotpass)
    else:
        return render_template('accounts/olividar_contraseña.html', form=forgotpass)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
