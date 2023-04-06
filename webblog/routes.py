from flask import render_template, flash, redirect, url_for, request
from webblog import app, database, bcrypt
from webblog.forms import FormLogin, FormCriarConta, FormEditarPerfil  # recomendado detalhar o caminho
from webblog.models import Usuario  # conforme mencionado acima, poderia suprimir o 'webblog.'
from flask_login import login_user, logout_user  # método que realiza o login e logout
from flask_login import current_user  # método que verifica o usuário que está mexendo na página naquele momento
# também possui o parâmetro de verificar se está logado ou não
from flask_login import login_required
# função que usamos como um decorator, para controle/bloqueio de páginas por usuários não logados

lista_usuarios = ['Victor', 'Yasmin']  # definindo lista de usuarios do blog


# route é método que faz parte da classe Flask, o @ antes significa que é um decorator, é uma função que atribui uma
# nova funcionalidade para a função que vem abaixo dele, ou seja, a função home tem a funcionalidade de exibir
# o seu codigo quando o link '/' for acionado, ou seja, homepage
@app.route('/')  # mostra o caminho (URL) de onde a página será mostrada, nesse caso é a homepage
def home():  # função que informa o que será mostrado na página, usaremos a pasta 'templates' para arquivos HTML
    return render_template('home.html')  # função que diz qual arquivo HTML na pasta 'templates' será carregado


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required  # com isso, somente quem está logado terá acesso à página
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)  # o primeiro parametro pode ser o nome
    # que quiser, ja o segundo seria a lista criada anteriormente no python (por padrao usa o mesmo nome), pois
    # o segundo nome vai ser a variavel python dentro do html em 'usuarios', estamos passando essa variavel pro HTML


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
            # passando parametros da função flash, a mensagem (.data para pegar o valor preenchido)
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
        # criando um novo usuario, instanciando a classe Usuario() - cada usuário seria um novo objeto
        database.session.add(usuario)  # adicionando a variável usuario à sessão do banco de dados
        database.session.commit()  # inserindo os dados no banco de dados
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


@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if request.method == "GET":  # caso a operação seja GET (default) traz as informações do usuário para os campos
        form.username.data = current_user.username
        form.email.data = current_user.email
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)
