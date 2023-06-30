""" Este arquivo serve como inicializador do app, contendo as configurações iniciais do Flask. Toda vez que o webblog
for chamado, ele é executado """

import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # (install flask-sqlalchemy) para usar o banco de dados
from flask_login import LoginManager  # (install flask-login) para validar dados de login
from flask_bcrypt import Bcrypt  # (install flask_bcrypt) para criptografia de senhas
import os  # para auxiliar na conexão com o banco de dados PostgreSQL, no Railway, para manipular variáveis de ambiente

app = Flask(__name__)
app.config['SECRET_KEY'] = '952975e9b8f4856c555784420cf99476'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_de_dados.db'  # informa caminho onde o BD local será salvo

""" app = Flask(__name__) significa que o app é uma instancia da classe flask com o parâmetro name
indica ao flask que o arquivo é um site e conecta os demais códigos que irão compor o site(outros arquivos, HTML, etc)

o csrf token é uma ferramenta para criar uma camada de segurança junto aos formulários do seu site
serve para prevenir ataques ao backend do site, comunicação com o banco de dados e etc
o parametro 'SECRET_KEY' é uma chave secreta/token
para gerar um token usando o python, abrir o terminal e importar a biblioteca 'secrets', que gera token automaticamente
'python > import secrets > secrets.token_hex(16)' e depois digitar exit(), será gerado token hex com 16 caracteres
com isso, passamos uma configuração no nosso arquivo main para o app do flask, a chave do app """

# if os.getenv("DATABASE_URI"):  # pega a variável de ambiente do Banco de Dados PostgreSQL
#     # se a variável 'DATABASE_URL' existe, ou seja, se o código está sendo rodado pelo servidor, pega o BD de lá
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
#     print('\nConectado com banco de dados remoto.')
# else:
#     # caso contrário, utiliza o BD local
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_de_dados.db'
#     print('\nConectado com banco de dados local.')

""" acima temos a configuração de onde ficará o banco de dados do aplicativo
'DATABASE_URL' é o caminho local onde ficará o banco de dados, 'sqlite:///' por padrão seguido do nome do BD
significa que o BD será criado no mesmo local do programa, localmente
já a primeira clausula do if verifica se existe a variável de ambiente do BD do servidor"""

# criando instância do Bcrypt. Somente nosso site será capaz de criptografar/descriptografar
bcrypt = Bcrypt(app)

# declarando a variável para aplicar a classe login manager dentro do app
login_manager = LoginManager(app)

# criando BD em formato de classes, instanciando de acordo com as configurações que setamos para o app
database = SQLAlchemy(app)

# login_view mostrará a página em que o usuário será redirecionado caso seja página onde o login é exigido
# deve-se passar como um texto o nome da função pra onde você quer que seja direcionado
login_manager.login_view = 'login'

# passando o parâmetro que define a categoria do alerta ao ser redirecionado
login_manager.login_message_category = 'alert-info'

""" Essa importação é necessária para que a base de dados seja criada com as tabelas. Se não tiver, a base de dados é
criada sem as tabelas de Post e Usuario. Importamos nesse lugar pois as variáveis são criadas somente acima, evitando o
problema de importação circular """
from webblog import models

# cria uma engine para avaliar o BD, passando o link do BD
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    # verifica se tem a tabela usuario, tem que ser com o U minusculo
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Banco de dados criado.")
        # se não tem a tabela, faz o drop e o create na sequencia, recriando o BD
else:
    print("Banco de dados já existente.")
    # se já tem a tabela, só printa para sabermos dessa informação

from webblog import routes
# é necessário executar o arquivo routes para colocar os links no ar
# diferentemente das demais importações, essa tem que vir por último, pois o routes precisa do app, que é criado acima
