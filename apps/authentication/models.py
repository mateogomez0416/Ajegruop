# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass
import datetime
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import relationship
from flask import  redirect, url_for



class UserBase(db.Model, UserMixin):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def update(self, **kwargs):
        print(kwargs.items())
        mydict={}
        for field, value in kwargs.items():
            if field in dir(self):
                print("esta")
                if value is not None:
                    mydict[field]=value
                    print(self,"=>esto es self")
                    print( field,"=> es el field ")
                    print( value, "=> esto es value ")
        print(mydict)       
        return mydict 
            



class Cargo(db.Model):

    __tablename__ = 'Cargo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),)
    empleado = relationship("Empleado", uselist=True, backref="Cargo")
    

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]


            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)
    def update(self, **kwargs):
        print(kwargs.items())
        mydict={}
        for field, value in kwargs.items():
            if field in dir(self):
                print("esta")
                if value is not None:
                    mydict[field]=value
                    print(self,"=>esto es self")
                    print( field,"=> es el field ")
                    print( value, "=> esto es value ")
        print(mydict)       
        return mydict 
            

class Dependencia(db.Model):

    __tablename__ = 'Dependencia'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    empleado = relationship("Empleado", uselist=True, backref="Dependencia")

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]


            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)
    def update(self, **kwargs):
        print(kwargs.items())
        mydict={}
        for field, value in kwargs.items():
            if field in dir(self):
                print("esta")
                if value is not None:
                    mydict[field]=value
                    print(self,"=>esto es self")
                    print( field,"=> es el field ")
                    print( value, "=> esto es value ")
        print(mydict)       
        return mydict 
            

class Permisos(db.Model):

    __tablename__ = 'Permisos'

    id = db.Column(db.Integer, primary_key=True)
    editar = db.Column(db.String(10),)
    crear = db.Column(db.String(10),)
    eliminar = db.Column(db.String(10),)
    empleado = db.Column(db.Integer, ForeignKey('Empleado.id'))
    
    

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]


            setattr(self, property, value)

    def update(self, **kwargs):
            print(kwargs.items())
            mydict={}
            for field, value in kwargs.items():
                if field in dir(self):
                    print("esta")
                    if value is not None:
                        mydict[field]=value
                        print(self,"=>esto es self")
                        print( field,"=> es el field ")
                        print( value, "=> esto es value ")
            print(mydict)       
            return mydict 



class Empleado(UserBase):

    __tablename__ = 'Empleado'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),)
    apellido = db.Column(db.String(64),)
    cedula = db.Column(db.String(64),unique=True )
    direccion = db.Column(db.String(64),)
    celular = db.Column(db.String(64),)
    rh = db.Column(db.String(64),)
    fecha_naci = db.Column(db.String(64),)
    salario = db.Column(db.Float,)
    tipo_contrato = db.Column(db.String(64),)
    fecha_inicio = db.Column(db.String(64),)
    fecha_terminacion = db.Column(db.String(64),) 
    genero  = db.Column(db.String(64),)
    ciudad_nacimiento = db.Column(db.String(64),)
    estado = db.Column(db.String(64),)

    role = db.Column(db.String(64),)###
    
    retroalimentacion = relationship("RetroAlimentacion", uselist=True, backref="Empleado")
    cargo=db.Column(db.Integer, ForeignKey('Cargo.id'))
    dependencia=db.Column(db.Integer, ForeignKey('Dependencia.id'))
    permisos=relationship("Permisos", uselist=True, backref="Empleado")
    
    def __repr__(self):
        dependencia=Dependencia.query.filter_by(id=self.dependencia).first()
        cargo=Cargo.query.filter_by(id=self.cargo).first()
        return str(self.name + " " +self.apellido +" "+self.cedula+ " "+ dependencia.name + " " + cargo.name)


class RetroAlimentacion(db.Model):

    __tablename__ = 'RetroAlimentacion'

    id = db.Column(db.Integer, primary_key=True)
    calificacion = db.Column(db.Float, )
    observacion = db.Column(db.Text(),)
    fecha_retro = db.Column(db.Date, default=datetime.datetime.now)
    empleado=db.Column(db.Integer, ForeignKey('Empleado.id'))

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]


            setattr(self, property, value)

    def __repr__(self):
        return str(self.fecha_retro)




@login_manager.user_loader
def user_loader(id):
    return Empleado.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Empleado.query.filter_by(username=username).first()
    return user if user else None
