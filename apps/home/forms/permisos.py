from typing import List
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,SelectField,FloatField, BooleanField, RadioField
from wtforms.validators import Email, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from apps.authentication.models import Cargo,Dependencia,Empleado, Permisos

def query_factory():
    return Empleado.query


class ShowPermisosForm(FlaskForm):
    editar = RadioField('editar',
                         id='name_editar',
                         choices=[('Editar'),('No Editar')]
                        #  validators=[DataRequired()]
                        ) 
    
    crear = RadioField('crear',
                         id='name_crear',
                         choices=[('Crear'),('No Crear')]
                        #  validators=[DataRequired()]
                        ) 

    eliminar = RadioField('eliminar',
                         id='name_eliminar',
                         choices=[('Eliminar'),('NoEliminar')]
                        #  validators=[DataRequired()]
                        ) 

    empleado = QuerySelectField(query_factory = query_factory,allow_blank=True, validators=[DataRequired()])
                         