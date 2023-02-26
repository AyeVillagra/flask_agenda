# funcion que invoca el motor de plantilas Jinja2; sustituye en el renderizado los bloques con los
# valores correspondientes dados por los argumentos proporcionados en la llamada de la función (línea 19)

from flask import render_template, flash, redirect, url_for, request

from app import app
from app import db
from flask_login import current_user, login_user, login_required, logout_user
from app.forms import LoginForm, RegistrationForm, CreateContactForm
from app.models import User, Contact
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return render_template('index.html', background=current_user.background_color, title='Home')

    return render_template('index.html',
                           title='Home')  # si no se pasa un valor para title, la plantilla da uno predeterminado


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # current_user, variable utilizada para obtener el objeto usuario que representa al cliente que hace la petición
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user.password_hash)
        print(form.password.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)  # función que registra al usuario como conectado
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':  # url_parse determina si una url es relativa o absoluta
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        print(user.password_hash)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/contacts', methods=['GET'])
def contacts():
    if current_user.is_authenticated:
        contacts = Contact.query.with_entities(Contact.contactname).join(User,User.id == Contact.user_id).filter(User.id==current_user.id).all()
        print(contacts)
        return render_template('contact.html', contacts=contacts, title='Mis Contactos')


@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    form = CreateContactForm()
    if form.validate_on_submit():
        contact = Contact()
        contact.contactname = form.contactname.data
        contact.celularnumber = form.celularnumber.data
        contact.description = form.description.data
        contact.user_id = current_user.id
        db.session.add(contact)
        db.session.commit()
        flash('Contacto agregado con éxito')
        return redirect(url_for('contacts'))

    return render_template('form_contact.html', form=form)


# quiero guardar la preferencia de color del usuario ya logueado
@app.route('/save_preference', methods=['POST'])
def save_preference():
    background_color = request.form['background_color']
    print(background_color)
    current_user.background_color = background_color
    db.session.add(current_user)
    db.session.commit()
    flash('Preferencia guardada')
    return redirect(url_for('index'))


# guarda el color y recarga la página para aplicar el color de fondo (ver index línea 18 - agregué un IF porque
# sino no se puede iniciar sesión ya que no tiene el atributo background color)


@app.route('/get_preference', methods=['GET'])
def get_preference():
    username = request.args.get('username')  # recupera el nombre de usuario
    user = User.query.filter_by(username=username).first()  # (consulta DB)
    return user.background_color  # retorna el color guardado para el usario
