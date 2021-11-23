# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,SelectField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = TextField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    role = SelectField('Role',
                         id='role_create',
                         choices=[('Empleado'),('Admin'),('SuperAdmin')],
                         validators=[DataRequired()])


class CambiarContraseñaForm(FlaskForm):
    password1 = PasswordField('Password',
                             id='pwd_change1',
                             validators=[DataRequired()])
    
    password2 = PasswordField('Password',
                             id='pwd_change2',
                             validators=[DataRequired()])
                    
class ForgotPass(FlaskForm):
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])