from myproject.extensions import db, lm
from myproject.models.class_usuario import Usuario
from datetime import datetime
from flask_login import UserMixin


@lm.user_loader  # informs login manager that the function below returns user id
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))  # validates user during login


# UserMixin is a parameter to define all necessities that login manager will need to manage login process
class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    corpo = db.Column(db.Text, nullable=False)
    # defining creation date as the same as system date using utcnow function without () to get actual creation date
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # making reference to post author as a FK from Usuario class (required to not use capital letters in here)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)