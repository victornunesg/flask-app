from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user
from myproject.extensions import db
from myproject.models.class_post import Post
from myproject.models.forms import FormCriarPost, FormEditarPost

posts_bp = Blueprint('posts_bp', __name__, template_folder='templates')


@posts_bp.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        db.session.add(post)  # adicionando a variável usuario à sessão do banco de dados
        db.session.commit()  # inserindo os dados no banco de dados
        flash('Post criado com sucesso!', 'alert-success')
        return redirect(url_for('public_pages_bp.home'))
    return render_template('criarpost.html', form=form)


@posts_bp.route('/post/<post_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get(post_id)
    form = FormEditarPost()
    #  Traz as informações atuais do post para os campos do formulário
    if request.method == "GET":
        form.titulo.data = post.titulo
        form.corpo.data = post.corpo
    elif form.validate_on_submit() and 'botao_submit' in request.form:
        post.titulo = form.titulo.data
        post.corpo = form.corpo.data
        # o post já existe, portanto posso dar o commit diretamente, sem a necessidade do session.add
        db.session.commit()
        flash(f'Post editado com sucesso!', 'alert-success')
        return redirect(url_for('public_pages_bp.home'))

    return render_template('editarpost.html', post=post, form=form)


@posts_bp.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
# <post_id> significa que iremos passar uma varíavel no link ao chamar a página, para exibir um post específico
# a função de exibir o post também recebe o post_id como parâmetro
def exibir_post(post_id):
    post = Post.query.get(post_id)  # retornando o post que tem o id igual ao post_id (get pega pela chave primária)
    return render_template('post.html', post=post)


@posts_bp.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        db.session.delete(post)
        db.session.commit()
        flash('Post excluído com sucesso', 'alert-danger')
        return redirect(url_for('public_pages_bp.home'))
    else:
        abort(403)  # o abort informa mensagem de erro 403 (Forbidden)
