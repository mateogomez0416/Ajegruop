from flask_wtf import FlaskForm
from wtforms import TextAreaField, FloatField
from wtforms.validators import  DataRequired,NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from apps.authentication.models import Empleado

def empleado_query():
    return Empleado.query.filter_by(role='Empleado')


class CreateRetroAlimentacionForm(FlaskForm):
    

    calificacion = FloatField('calificacion',
                         id='calificacion_create',
                        
                         render_kw = {"class": "form-control ", "type":"number"  ,"min":"1", "max":"100" },
                         validators=[DataRequired(), NumberRange(min=1, max=100, message="Valores de 1 a 100")])
    observacion = TextAreaField('observacion',
                         id='observacion_create',
                         render_kw = {"class": "form-control ", },
                         validators=[DataRequired()])
    
    empleado = QuerySelectField(query_factory=empleado_query,allow_blank=True, validators=[DataRequired()])
   
