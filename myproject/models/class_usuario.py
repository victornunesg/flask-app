from myproject.extensions import db, lm
from flask_login import UserMixin


@lm.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    cursos = db.Column(db.String, nullable=False, default='Não informado')
    foto_perfil = db.Column(db.String, nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='autor', lazy=True)

    def contar_posts(self):
        return len(self.posts)
