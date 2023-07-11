from myproject.extensions import db, lm
from myproject.models.class_usuario import Usuario
from datetime import datetime
from flask_login import UserMixin


@lm.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    corpo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)