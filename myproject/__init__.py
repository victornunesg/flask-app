from flask import Flask
from myproject.extensions import db, lm, database_initializer, bcrypt  # importing database and login_manager
from public_pages.public_pages import public_pages_bp
from users.users import users_bp
from posts.posts import posts_bp
from profiles.profiles import profiles_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = '952975e9b8f4856c555784420cf99476'

# initializing DB
database_initializer(app)

# creates object bcrypt to encrypt/decrypt
bcrypt.init_app(app)

# creates object login_manager
lm.init_app(app)

# login_view redirects user to 'login' page wherever login is necessary to proceed, calls 'login' function
lm.login_view = 'users_bp.login'

# defines alert category when login is done
lm.login_message_category = 'alert-info'

app.register_blueprint(public_pages_bp)
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(profiles_bp)
