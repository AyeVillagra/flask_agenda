from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin #clase que incluye implementaciones genéricas para los modelos de usuario

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) #este id es un string - ver compatibilidad con la DB

#db.Model es una clase base de flask-sqlalchemy
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    background_color = db.Column(db.String(80))
    contacts = db.relationship('Contact', backref='user', lazy='dynamic')


#método que indica cómo imprimir objetos de esta clase
    def __repr__(self):
        return '<User {}>'.format(self.username)

#métodos de hashing de contraseña
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contactname = db.Column(db.String)
    celularnumber = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Contact {}>'.format(self.celularnumber, self.contactname)
