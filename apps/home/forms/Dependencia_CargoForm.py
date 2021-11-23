from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import  DataRequired


class CreateDependencia_CargoForm(FlaskForm):

     name=StringField('Nombre',id='name',validators=[DataRequired()] ,render_kw = {"class": "form-control"  })
     
   
