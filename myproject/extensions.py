# file to input extensions that app may have to avoid circular reference error
import os
import sqlalchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

lm = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()


def database_initializer(app):

    # defining URL for database
    if os.getenv("DATABASE_URL"):  # if gets server ambience variable (PostgreSQL)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
        print('\nRunning by the Rail server, using PostgreSQL db.')
    else:
        print('\nRunning locally, using SQLITE db.')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'local_database.db')

    # creates the database for the app
    db.init_app(app)

    # checking DB consistency, if user table exists, the structure is correct
    engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table("usuario"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("New DB created.")
    else:
        print("Existing DB found.")






