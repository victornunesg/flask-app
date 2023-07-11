from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, login_user, logout_user
from myproject.extensions import bcrypt, db
from myproject.models.class_usuario import Usuario
from myproject.models.forms import FormCriarConta, FormLogin

users_bp = Blueprint('users_bp', __name__, template_folder='templates')


@users_bp.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@users_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        db.session.add(usuario)  # adicionando a variável usuario à sessão do banco de dados
        db.session.commit()  # inserindo os dados no banco de dados
        login_user(usuario)  # realiza o login na sequência
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('public_pages_bp.home'))

    return render_template('cadastro.html', form_criarconta=form_criarconta)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()  # form_login será instância da classe FormLogin(), em forms.py
    # se o formulario de login for validado ao clicar em submit no botão de login
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('public_pages_bp.home'))  # redirecionando o usuário para a homepage
        else:
            flash('Falha no login, e-mail ou senha incorretos', 'alert-danger')

    return render_template('login.html', form_login=form_login)


@users_bp.route('/sair')
@login_required
def sair():
    logout_user()  # realiza o logout do usuário automaticamente
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('public_pages_bp.home'))
