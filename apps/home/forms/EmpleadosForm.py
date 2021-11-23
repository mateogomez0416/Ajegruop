from typing import List
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,SelectField,FloatField
from wtforms.validators import Email, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from apps.authentication.models import Cargo,Dependencia,Empleado

def cargo_query():
    return Cargo.query

def dependencia_query():
    return Dependencia.query

class CreateEmpleadoForm(FlaskForm):

        
    name = TextField('Name',
                         id='name_create',
                         validators=[DataRequired()]) 
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    apellido = TextField('Apellido',
                         id='apellido_create',
                         validators=[DataRequired()])
    cedula = TextField('Cedula',
                            id='cedula_create',
                            validators=[DataRequired()])
    direccion = TextField('Direccion',
                            id='direccion_create',
                            validators=[DataRequired()])
    celular = TextField('Celular',
                            id='celular_create',
                            validators=[DataRequired()])
    rh = SelectField('Rh',
                            id='rh_create',
                            choices=[('A +'),('A-'),('B +'),('B-'),('AB+'),('AB-'),('O+'),('O-')],
                            validators=[DataRequired()])

    fecha_naci = TextField('Fecha de nacimiento',
                         id='fecha_naci_create',
                         render_kw = {"class": "form-control ","data-datepicker":"", "pattern" :"\d{4}-\d{2}-\d{2}" },
                         validators=[DataRequired()])
    salario = FloatField('salario',
                         id='salario_create',
                         validators=[DataRequired()])
    tipo_contrato = SelectField('Tipo de contrato',
                         id='tipo_contrato_create',
                         choices=[('prestación de servicios.'),('término Indefinido'),('de aprendizaje')],
                         validators=[DataRequired()])
    fecha_inicio = TextField('Fecha de inicio',
                         id='fecha_inicio_create',
                          render_kw = {"class": "form-control ","data-datepicker":"" },
                         validators=[DataRequired()])
    fecha_terminacion = TextField('Fecha de terminacion',
                         id='fecha_terminacion_create',
                          render_kw = {"class": "form-control ","data-datepicker":"" },
                         validators=[DataRequired()])
    genero = SelectField('genero',
                         id='genero_create',
                         choices=[('Femenino'),('Masculino'),('otro')],
                         validators=[DataRequired()])
    ciudad_nacimiento = TextField('Ciudad de nacimiento',
                         id='ciudad_nacimiento_create',
                         validators=[DataRequired()])
    estado = SelectField('Estado',
                         id='estado_create',
                         choices=[('Activo'),('Inactivo'),('Suspendido')],
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    role = SelectField('Role',
                         id='role_create',
                         choices=[('Empleado'),('Admin'),('SuperAdmin')],
                         validators=[DataRequired()])

    cargo = QuerySelectField(query_factory=cargo_query,allow_blank=True,get_label='name')
    dependencia = QuerySelectField(query_factory=dependencia_query,allow_blank=True,get_label='name')
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])

class ShowEmpleadoForm(FlaskForm):
    name = TextField('Name',
                         id='name_create',
                         validators=[DataRequired()]) 
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    apellido = TextField('Apellido',
                         id='apellido_create',
                         validators=[DataRequired()])
    cedula = TextField('Cedula',
                            id='cedula_create',
                            validators=[DataRequired()])
    direccion = TextField('Direccion',
                            id='direccion_create',
                            validators=[DataRequired()])
    celular = TextField('Celular',
                            id='celular_create',
                            validators=[DataRequired()])
    rh = TextField('Rh',
                            id='rh_create',
                            validators=[DataRequired()])

    fecha_naci = TextField('Fecha de nacimiento',
                         id='fecha_naci_create',
                         render_kw = {"class": "form-control ","data-datepicker":"", "pattern" :"\d{4}-\d{2}-\d{2}" },
                         validators=[DataRequired()])
    salario = FloatField('salario',
                         id='salario_create',
                         validators=[DataRequired()])
    tipo_contrato = TextField('Tipo de contrato',
                         id='tipo_contrato_create',
                         validators=[DataRequired()])
    fecha_inicio = TextField('Fecha de inicio',
                         id='fecha_inicio_create',
                          render_kw = {"class": "form-control ","data-datepicker":"" },
                         validators=[DataRequired()])
    fecha_terminacion = TextField('Fecha de terminacion',
                         id='fecha_terminacion_create',
                          render_kw = {"class": "form-control ","data-datepicker":"" },
                         validators=[DataRequired()])
    genero = TextField('genero',
                         id='genero_create',
                         validators=[DataRequired()])
    ciudad_nacimiento = TextField('Ciudad de nacimiento',
                         id='ciudad_nacimiento_create',
                         validators=[DataRequired()])
    estado = TextField('Estado',
                         id='estado_create',
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    role = TextField('Role',
                         id='role_create',
                         validators=[DataRequired()])

    cargo =TextField('Cargo',
                         id='cargo_create',
                         validators=[DataRequired()])

    dependencia = TextField('Dependencia',
                         id='dependencia_create',
                         validators=[DataRequired()])

  
   
    