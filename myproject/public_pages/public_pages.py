from flask import Blueprint, render_template
from myproject.models.class_post import Post

public_pages_bp = Blueprint('public_pages_bp', __name__, template_folder='templates')


@public_pages_bp.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@public_pages_bp.route('/contato')
def contato():
    return render_template('contato.html')
