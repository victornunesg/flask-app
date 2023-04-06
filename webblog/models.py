# models.py é o arquivo criado para armazenar os modelos/tabelas do BD (nomenclatura do arquivo é padrão)
# para funcionar, temos que importar o banco de dados SQLAlchemy no arquivo init

from webblog import database, login_manager
from datetime import datetime  # para preenchimento de data/hora do post
from flask_login import UserMixin
# UserMixin é um parâmetro que vamos passar para a classe Usuarios, que irá atribuir a ela todas as caracteristicas
# que o login manager vai precisar para gerenciar o processo de login


@login_manager.user_loader  # decorator para informar ao login manager que a função abaixo retorna o ID de usuario
def load_usuario(id_usuario):  # função para validação de usuário durante o login
    # o método get verifica a primary key do BD, não sendo necessário usar o filter_by ou first, etc
    return Usuario.query.get(int(id_usuario))  # somente retornando a validação de ID do usuário, retornando o usuário


# herda a classe Model com a série de atributos, basta basicamente definir colunas agora
# também recebe de parâmetro o UserMixin para poder comunicar com o login manager
class Usuario(database.Model, UserMixin):
    # cada informação seria uma coluna na tabela usuário no banco de dados, definindo chave primaria para ID
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)  # campo não pode ser vazio, preenchimento obrigatório
    email = database.Column(database.String, nullable=False, unique=True)  # campo deve ser único
    senha = database.Column(database.String, nullable=False)
    cursos = database.Column(database.String, nullable=False, default='Não informado')
    foto_perfil = database.Column(database.String, nullable=False, default='default.jpg')
    # foto é string pois iremos indicar o nome do arquivo da foto, sendo padrão um avatar genérico

    posts = database.relationship('Post', backref='autor', lazy=True)
    # cria o relacionamento com a tabela de posts do banco de dados (1 usuario pode ter vários posts)
    # o nome do parametro backref é o nome que iremos chamar dentro de Post para obter a informação do usuário que criou
    # lazy=True seria para obter todas as informações do banco de dados


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)  # informando ao BD que será um texto ao invés de String
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    # valor padrão data/hora atual do sistema, passando a função utcnow (sem parenteses) para não acontecer de
    # todos os posts serem armazenados na mesma data/hora no banco de dados
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    # criando a coluna que faz referência ao autor do post, do relacionamento com a tabela usuários
    # obrigatoriamente, na chave estrangeira, o nome da classe do usuario deve estar em letras minusculas
