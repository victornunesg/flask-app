from myproject.extensions import db, lm
from flask_login import UserMixin


@lm.user_loader  # informs login manager that the function below returns user id
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))  # validates user during login


# UserMixin is a parameter to define all necessities that login manager will need to manage login process
class Usuario(db.Model, UserMixin):
    # each attribute is a column in the DB
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    cursos = db.Column(db.String, nullable=False, default='Não informado')
    foto_perfil = db.Column(db.String, nullable=False, default='default.jpg')  # string because is a path to the photo

    # creating relationship with posts table from DB.
    # backref is the name we can call inside Post to get the information of who created the post
    # lazy=True to get all the information from the DB
    posts = db.relationship('Post', backref='autor', lazy=True)

    def contar_posts(self):
        return len(self.posts)  # returns user's post quantity
