# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from operator import length_hint
from sqlalchemy.orm.base import instance_dict
import yagmail as yagmail
from apps import db
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.authentication.models import Dependencia,Cargo, Empleado, Permisos, RetroAlimentacion
from apps.authentication.forms import CambiarContraseñaForm
from .forms.Dependencia_CargoForm import CreateDependencia_CargoForm
from.forms.RetroAlimentacionForm import CreateRetroAlimentacionForm
from .forms.EmpleadosForm import CreateEmpleadoForm,ShowEmpleadoForm
from .forms.permisos import ShowPermisosForm
import datetime
from flask import redirect, url_for
def only_admin():
    print('kbvhkdfbldskhf: ',current_user.role)
    if current_user.role=="Empleado":
        return True


@blueprint.route('/dashboard')
@login_required
def dashboard():
    user_list=Empleado.query.all()
    
    return render_template('home/transactions.html', segment='transactions',user_list=user_list)

@blueprint.route('/mi-retroalimentacion')
@login_required
def mi_retroalimentacion():
    retro_list=RetroAlimentacion.query.filter_by( empleado=current_user.id).all()
    suma= 0
    cont = 0
    for i in retro_list:
        suma += i.calificacion
        cont += 1

    prom = round(suma/cont,2)

    return render_template('home/dashboard.html', segment='dashboard',retro_list=retro_list, promedio=prom )


@blueprint.route('/add-dependencia', methods=['GET', 'POST'])
@login_required
def add_dependencia():

    # print(only_admin())
    # if only_admin()==True:
    form=CreateDependencia_CargoForm(request.form)
    msg=''
    print(request.form )
    if 'add_dependencia' in request.form:
        name=request.form['name']
        dependencia=Dependencia.query.filter_by(name=name).first()
        if dependencia:
            msg='Dependencia already registered'
        else:
            if form.validate_on_submit():
                dependencia= Dependencia(**request.form)
                db.session.add(dependencia)
                db.session.commit()
                msg='Dependencia agregada'
            else:
                msg='Datos no validos'
    form=CreateDependencia_CargoForm()
    dependencia_list=Dependencia.query.all()
    return render_template('home/add_dependencia.html',msg=msg,form=form,dependencia_list=dependencia_list,segment='add_dependencia')
    # else:
    #     return redirect(url_for('home_blueprint.info_empleado'))


@blueprint.route('/add-cargo', methods=['GET', 'POST'])
@login_required
def add_cargo():
    form=CreateDependencia_CargoForm(request.form)
    msg=''
    if 'add_cargo' in request.form:
        name=request.form['name']
        cargo=Cargo.query.filter_by(name=name).first()
        if cargo:
            msg='cargo already registered'
        else:
            print(form.validate_on_submit())
            if form.validate_on_submit():
                cargo= Cargo(**request.form)
                print('cargo: ', cargo)
                db.session.add(cargo)
                db.session.commit()
                msg='cargo agregada'
            else:
                msg='Datos no validos'
    form=CreateDependencia_CargoForm()
    cargo_list=Cargo.query.all()
    return render_template('home/add_cargo.html',msg=msg,form=form,cargo_list=cargo_list,segment='add_cargo')



@blueprint.route('/Permisos', methods=['GET', 'POST'])
@login_required
def permisos():
    # editar = request.form['editar']
    # eliminar = request.form['eliminar']
    # crear = request.form['crear']

    # if request.form['editar'] == 'y'
    form=ShowPermisosForm(request.form)
    msg=''
    print('request:  ',request.form)
    if 'add_permisos' in request.form:
        # name=request.form['name']
        # cargo=Cargo.query.filter_by(name=name).first()
        # if cargo:
        #     msg='cargo already registered'
        # else:
        #     print(form.validate_on_submit())
        if form.validate_on_submit():
            perm= Permisos(**request.form)
            print('permisos: ', perm)
            db.session.add(perm)
            db.session.commit()
            msg='Permisos Asignados'
        else:
            msg='Datos no validos'
    # form=ShowPermisosForm()
    perm_list=Permisos.query.all()
    return render_template('home/permisos.html',msg=msg,form=form,perm_list=perm_list,segment='add_permisos')


@blueprint.route('/empleado/', methods=['GET', 'POST'])
@login_required
def empleado():
    form=CreateEmpleadoForm(request.form)
    msg=''
    if 'add_empleado' in request.form:
        cedula=request.form['cedula']
        empleado=Empleado.query.filter_by(cedula=cedula).first()
        if empleado:
            msg='em already registered'
        else:
            print(form.validate_on_submit())
            if form.validate_on_submit():
                empleado= Empleado(**request.form)
                # print('empleado: ',empleado)
                db.session.add(empleado)
                db.session.commit()
                msg='empleado agregado'
                decode=request.form['password']
                email=empleado.email
                yag = yagmail.SMTP('componentepractico9@gmail.com', '1810Uninorte')
                yag.send(to= email, subject='Cuenta empleado', contents='nombre de cuenta: '+empleado.username+'\n'+'contraseña: '+decode)
                return redirect(url_for("home_blueprint.usuariosAll"))
            else:
                print(form.errors)
                msg=form.errors.values()
    form=CreateEmpleadoForm()
    return render_template('home/empleado.html',msg=msg,form=form,segment='empleado')


# =============
@blueprint.route('/EditUser/<int:id>/', methods=['GET', 'POST'])
@login_required
def EditUser(id):
    empleado = Empleado.query.get(id)
    form=ShowEmpleadoForm(request.form, obj=empleado)
    #form=CreateEmpleadoForm(request.form, obj=empleado)
    msg=''
    if 'add_empleado' in request.form:
        #cedula=request.form['cedula']
        #empleado=Empleado.query.filter_by(cedula=cedula).first()
        if empleado:
            print(form.validate_on_submit())
            if form.validate_on_submit():
                print('request: ',request.form)
                print(dir(empleado))
                fields= empleado.update(**form.data)
                #print('empleado: ',empleado)
                num_rows_updated = Empleado.query.filter_by(id=id).update(fields)
                # db.session.add(empleado)
                db.session.commit()
                msg='empleado agregado'
                # decode=request.form['password']
                # email=empleado.email
                # yag = yagmail.SMTP('componentepractico9@gmail.com', '1810Uninorte')
                # yag.send(to= email, subject='Cuenta empleado', contents='nombre de cuenta: '+empleado.username+'\n'+'contraseña: '+decode)
                return redirect(url_for("home_blueprint.usuariosAll"))
            else:
                print(form.errors)
                msg=form.errors.values()

        else:
            msg='Empleado no existe'
                # form=CreateEmpleadoForm()
    return render_template('home/empleado.html',msg=msg,form=form,segment='empleado')
# ===========

@blueprint.route('/usuariosAll/', methods=['GET', 'POST'])
@login_required
def usuariosAll():
    lista_usuarios = Empleado.query.all()
    return render_template('home/usuariosAll.html',segment='usuariosAll',  usuarios = lista_usuarios)


@blueprint.route('/usuarios_elim/<int:id>/', methods=['GET', 'POST'])
@login_required
def usuarios_elim(id):
    delete_user = Empleado.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    return redirect(url_for("home_blueprint.usuariosAll"))


@blueprint.route('/permiso_elim/<int:id>/', methods=['GET', 'POST'])
@login_required
def permiso_elim(id):
    delete_user = Permisos.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    return redirect(url_for("home_blueprint.permisos"))


@blueprint.route('/cargo_elim/<int:id>/', methods=['GET', 'POST'])
@login_required
def cargo_elim(id):
    delete_user = Cargo.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    return redirect(url_for("home_blueprint.add_cargo"))

@blueprint.route('/dependencia_elim/<int:id>/', methods=['GET', 'POST'])
@login_required
def dependencia_elim(id):
    delete_user = Dependencia.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    return redirect(url_for("home_blueprint.add_dependencia"))


# =============
@blueprint.route('/edit_cargo/<int:id>/', methods=['GET', 'POST'])
@login_required
def EditCargo(id):
    cargo = Cargo.query.get(id)
    form=CreateDependencia_CargoForm(request.form, obj=cargo)
    #form=CreateEmpleadoForm(request.form, obj=cargo)
    msg=''
    if 'add_cargo' in request.form:
        #cedula=request.form['cedula']
        #cargo=Empleado.query.filter_by(cedula=cedula).first()
        if cargo:
            print(form.validate_on_submit())
            if form.validate_on_submit():
                print('request: ',request.form)
                print(dir(cargo))
                fields= cargo.update(**form.data)
                #print('cargo: ',cargo)
                num_rows_updated = Cargo.query.filter_by(id=id).update(fields)
                # db.session.add(cargo)
                db.session.commit()
                msg='cargo editado'
                # decode=request.form['password']
                # email=cargo.email
                # yag = yagmail.SMTP('componentepractico9@gmail.com', '1810Uninorte')
                # yag.send(to= email, subject='Cuenta cargo', contents='nombre de cuenta: '+cargo.username+'\n'+'contraseña: '+decode)
                return redirect(url_for("home_blueprint.add_cargo"))
            else:
                print(form.errors)
                msg=form.errors.values()

        else:
            msg='Cargo no existe'
                # form=CreatecargoForm()
    return render_template('home/add_cargo.html',msg=msg,form=form,segment='cargo')
# ===========


# =============
@blueprint.route('/Editdependencia/<int:id>/', methods=['GET', 'POST'])
@login_required
def Editdependencia(id):
    dependencia = Dependencia.query.get(id)
    form=CreateDependencia_CargoForm(request.form, obj=dependencia)
    #form=CreateDependenciaForm(request.form, obj=dependencia)
    msg=''
    if 'add_dependencia' in request.form:
        #cedula=request.form['cedula']
        #dependencia=Dependencia.query.filter_by(cedula=cedula).first()
        if dependencia:
            print(form.validate_on_submit())
            if form.validate_on_submit():
                print('request: ',request.form)
                print(dir(dependencia))
                fields= dependencia.update(**form.data)
                #print('dependencia: ',dependencia)
                num_rows_updated = Dependencia.query.filter_by(id=id).update(fields)
                # db.session.add(dependencia)
                db.session.commit()
                msg='dependencia editada'
                # decode=request.form['password']
                # email=dependencia.email
                # yag = yagmail.SMTP('componentepractico9@gmail.com', '1810Uninorte')
                # yag.send(to= email, subject='Cuenta dependencia', contents='nombre de cuenta: '+dependencia.username+'\n'+'contraseña: '+decode)
                return redirect(url_for("home_blueprint.add_dependencia"))
            else:
                print(form.errors)
                msg=form.errors.values()

        else:
            msg='Dependencia no existe'
                # form=CreateDependenciaForm()
    return render_template('home/add_dependencia.html',msg=msg,form=form,segment='add_dependencia')
# ===========

@blueprint.route('/info_empleado' ,methods=['GET', 'POST'])
@login_required
def info_empleado():
    empleado=Empleado.query.filter_by(id=current_user.id).first()
    cargo=Cargo.query.filter_by(id=empleado.cargo).first()
    dependencia=Dependencia.query.filter_by(id=empleado.dependencia).first()
    form=ShowEmpleadoForm(request.form, obj=empleado)
    form.cargo.data=str(cargo.name)
    form.dependencia.data=str(dependencia.name)
    print(form.data)

    return render_template('home/empleado_data.html', segment='empleado_info',form=form)
 

@blueprint.route('/retroalimentacion', methods=['GET', 'POST'])
@login_required
def retroalimentacion():
    print(request.form)
    #print(request.form['calificacion'],type(request.form['calificacion']))
    print (datetime.datetime.now().date())
    form=CreateRetroAlimentacionForm(request.form)
    
    date_now=datetime.datetime.now().date()
    msg=''
    if 'add_retroalimentacion' in request.form:        
        empleado_id=request.form['empleado']
        empleado=Empleado.query.filter_by(id=empleado_id).first()
        if empleado:
            retroalimentacion=RetroAlimentacion.query.filter_by( fecha_retro=date_now, empleado=empleado_id).all()
            print(retroalimentacion,"resultado query  ")
            
            if retroalimentacion:
                 msg='retro alimentacion de ese empleado ya esta agregada'
            else:
                print(form.validate_on_submit())
                if form.validate_on_submit():
                    retro= RetroAlimentacion(**request.form)
                    db.session.add(retro)
                    db.session.commit()
                    msg='retro agregado'
                else:
                    print(form.errors)
                    msg=form.errors.values()
        else:
            msg='empleado no registered'
            
    form=CreateRetroAlimentacionForm()
    print(form.empleado)
    return render_template('home/retroalimentacion.html',msg=msg,form=form, segment='retroalimentacion')

@blueprint.route('/cambiar-contraseña' ,methods=['GET', 'POST'])
@login_required
def cambiar_contraseña():
    form=CambiarContraseñaForm()

    return render_template('accounts/cambiar_contraseña.html', segment='cambiar_contraseña',form=form)
 

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
