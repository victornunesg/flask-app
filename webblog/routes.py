from flask import render_template, flash, redirect, url_for, request, abort
from webblog import app, database, bcrypt
from webblog.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormEditarPost
from webblog.models import Usuario, Post  # poderíamos suprimir o 'webblog.', mas é recomendado detalhar o caminho
from flask_login import login_user, logout_user  # método que realiza o login e logout
from flask_login import current_user  # método que verifica o usuário que está mexendo na página naquele momento
# também possui o parâmetro de verificar se está logado ou não
from flask_login import login_required
# função que usamos como um decorator, para controle/bloqueio de páginas por usuários não logados

import secrets
import os
# secrets para gerar o código para atualizar imagem de perfil e OS para separar o nome da imagem da extensão

from PIL import Image  # biblioteca Pillow (install Pillow) para compactar a imagem de maneira fácil

# route é método que faz parte da classe Flask, o @ antes significa que é um decorator, é uma função que atribui uma
# nova funcionalidade para a função que vem abaixo dele, ou seja, a função home tem a funcionalidade de exibir
# o seu codigo quando o link '/' for acionado, ou seja, homepage


@app.route('/')  # mostra o caminho (URL) de onde a página será mostrada, nesse caso é a homepage
def home():  # função que informa o que será mostrado na página, usaremos a pasta 'templates' para arquivos HTML
    # ordenando a exibição dos Posts por ID

    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required  # com isso, somente quem está logado terá acesso à página
def usuarios():
    # pegando todos os usuários do banco de dados e armazenando na variável "lista_usuários"
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)
    # o primeiro parametro pode ser o nome que quiser, ja o segundo seria a lista criada anteriormente no python
    # (por padrao usa o mesmo nome), pois o segundo nome vai ser a variavel python dentro do html em 'usuarios',
    # estamos passando essa variavel pro HTML


@app.route('/login', methods=['GET', 'POST'])  # methods autoriza os métodos GET e POST para submissão do formulário
# por definição apenas o método GET é liberado, estamos liberando o POST para não dar erro ao submeter
def login():
    form_login = FormLogin()  # form_login será instância da classe FormLogin(), em forms.py
    form_criarconta = FormCriarConta()  # form_criarconta será instância da classe FormCriarConta()
    # se o formulario de login for validado ao clicar em submit no botão de login
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # chama o método login_user para confirmar o login do usuário (primeiro parâmetro)
            # também controla o 'lembrar dados de acesso', como segundo parâmetro 'remember', aceita booleano
            flash(f'Login feito com sucesso no e-mail {form_login.email.data}', 'alert-success')
            # passando parâmetros da função flash, a mensagem (.data para pegar o valor preenchido)
            # e a categoria, de acordo com a documentação do flask e bootstrap
            par_next = request.args.get('next')
            # verificar se há algum parâmetro next na URL para saber se mandaremos para outra página específica
            # o request.args coleta todos os parâmetros da URL caso não seja especificado
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))  # redirecionando o usuário para a homepage
        else:
            flash('Falha no login, e-mail ou senha incorretos', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # transformará a senha do usuário em criptografada
        # para verificar se as senhas batem, utiliza-se o método bcrypt.check_password_hash(SENHA1, SENHA2)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        # cria novo usuario, instanciando a classe Usuario() - cada usuário seria um novo objeto
        database.session.add(usuario)  # adicionando a variável usuario à sessão do banco de dados
        database.session.commit()  # inserindo os dados no banco de dados
        login_user(usuario)  # realiza o login na sequência
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)
    # passando as duas informações de formulário para o HTML 'login.html', para serem usados


@app.route('/sair')
@login_required
def sair():
    logout_user()  # realiza o logout do usuário automaticamente
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    # definindo a variável que armazenará o caminho da foto de perfil para jogar no HTML
    # current_user significa um objeto de Usuario, onde temos dentro do BD a foto de perfil (string)
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)  # adicionando a variável usuario à sessão do banco de dados
        database.session.commit()  # inserindo os dados no banco de dados
        flash('Post criado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    # gera código aleatório de 8bytes para evitar duplicidades de nome de foto no banco de dados
    codigo = secrets.token_hex(8)

    # separa o nome da imagem de sua extensão usando OS, armazena um em cada variável
    nome, extensao = os.path.splitext(imagem.filename)

    # junta novamente o nome da imagem adicionando o código gerado
    nome_arquivo = nome + codigo + extensao

    # define o caminho onde o arquivo será salvo, o app.root_path retorna o caminho do web-blog e o join junta tudo
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    # comprime o tamanho da imagem, pois no site é somente 400 por 400, variável tamanho é uma tupla com as dimensões
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    # salva a imagem na pasta static/fotos_perfil
    imagem_reduzida.save(caminho_completo)

    # retorna o novo nome da foto
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:  # se o campo estiver marcado, adiciona na lista de cursos
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)  # retornando uma string com os cursos separados por ;


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()

    # caso a operação seja GET (default) traz as informações atuais do usuário para os campos do formulário
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    # se o formulário de editar o perfil for validado ao clicar em submit, atualiza os dados no banco de dados
    if form.validate_on_submit() and 'botao_submit_editar_perfil' in request.form:
        current_user.email = form.email.data
        current_user.username = form.username.data
        # verifica se houve o upload de uma nova foto para poder atualizá-la
        if form.foto_perfil.data:
            # chama a função salvar_imagem para realizar o tratamento da foto enviada pelo usuário
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            # atualiza o campo foto_perfil do usuário para carregar a nova foto do perfil
            current_user.foto_perfil = nome_imagem

        # chama a função atualizar_cursos passando o formulário de parâmetro
        current_user.cursos = atualizar_cursos(form)

        database.session.commit()
        flash(f'Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))

    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
# <post_id> significa que iremos passar uma varíavel no link ao chamar a página, para exibir um post específico
# a função de exibir o post também recebe o post_id como parâmetro
def exibir_post(post_id):
    post = Post.query.get(post_id)  # retornando o post que tem o id igual ao post_id (get pega pela chave primária)
    if current_user == post.autor:
        form = FormEditarPost()
        #  Traz as informações atuais do post para os campos do formulário
        if request.method == "GET":
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit() and 'botao_submit' in request.form:
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            # o post já existe, portanto posso dar o commit diretamente, sem a necessidade do session.add
            database.session.commit()
            flash(f'Post editado com sucesso!', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None  # temos que colocar o None para não haver erro na passagem de parâmetros se o usuário não for autor
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)  # o abort informa mensagem de erro 403 (Forbidden)
