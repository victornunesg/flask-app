# # arquivo para testes de criação e consulta do banco de dados
# # está comentado para evitar erros durante a execução do programa

from webblog import app, database  # importando app e database
from webblog.models import Usuario, Post  # importando as classes Usuário e Post

# # todos os comandos no seu banco de dados deve estar contido em um with, conforme abaixo
# # ao rodar esses comandos, o arquivo com o banco de dados deve constar na pasta 'instance'

# =====================================
# # criando o banco de dados
# =====================================
#
# with app.app_context():
#     database.create_all()  # após criar a base pela primeira vez, deixar esse comando comentado


# =====================================
# # criando um novo usuario manualmente, passando as informações obrigatórias definidas na classe Usuario
# =====================================

# with app.app_context():
#     usuario = Usuario(username='vitor2', email='vitor2@gmail.com', senha='123456')
#     usuario2 = Usuario(username='vitor3', email='vitor3@gmail.com', senha='123456')
#     # usuários não estão no banco de dados, temos que adicionar essa informação na sessão do BD
#     # e após isso será inserido após um commit
#
#     # adicionando na sessão do BD
#     database.session.add(usuario)
#     database.session.add(usuario2)
#
#     # enviando os usuários criados nas variáveis 'usuario' e 'usuario2' para o banco de dados através do commit
#     # pode ser realizado apenas uma vez, no final das operações
#     database.session.commit()

# =====================================
# # fazendo consultas ao BD para verificar os usuarios
# =====================================
#
# with app.app_context():
#     meus_usuarios = Usuario.query.all()  # pegando todas as informações do BD
#     meus_posts = Post.query.all()
#     print(f'\nObtendo a lista de usuários com o query.all(): {meus_usuarios}')
#     primeiro_usuario = Usuario.query.first()  # pegando apenas o primeiro usuario da lista
#     primeiro_usuario = Usuario.query[0]  # pegando apenas o primeiro usuario da lista
#     segundo_usuario = meus_usuarios[1]  # pegando apenas o segundo usuario da lista
#
#     # pegando informações dos usuarios
#     print('\nObtendo informacoes dos usuarios')
#     print(f'Email primeiro usuario: {primeiro_usuario.email}')
#     print(f'ID primeiro usuario: {primeiro_usuario.id}')
#     print(f'Qtde de posts primeiro usuario: {primeiro_usuario.posts}')
#
#     # utilizando busca com critérios no banco de dados, usando condições, como o e-mail por exemplo
#     usuario_teste = Usuario.query.filter_by(email='vitor3@gmail.com').first()
#     print(f'\nUsuario com o email = vitor3@gmail.com: {usuario_teste}')
#     print(f'Username do usuario com o email = vitor3@gmail.com: {usuario_teste.username}')
#
# with app.app_context():
#     meus_usuarios = Usuario.query.all()  # pegando todas as informações do BD
#     meus_posts = Post.query.all()
#     print('\nListando todas as informacoes de Usuário no Banco de Dados:')
#     for usuario in meus_usuarios:
#         print(f'Username: {usuario.username}')
#         print(f'Email: {usuario.email}')
#         print(f'Senha: {usuario.senha}')
#         print(f'Cursos: {usuario.cursos}')
#         print(f'Foto do Perfil: {usuario.foto_perfil}')
#         print('\n')
#
#     print('\nListando todos os Posts no Banco de Dados')
#     for posts in meus_posts:
#         print(f'ID: {posts.id}')
#         print(f'ID Usuario: {posts.id_usuario}')
#         print(f'Data de criacao: {posts.data_criacao}')
#         print(f'Titulo: {posts.titulo}')
#         print(f'Corpo: {posts.corpo}')


# =====================================
# # criando um post para cada usuario
# =====================================

# with app.app_context():
#     meu_post = Post(id_usuario=1, titulo='Meu primeiro post no blog', corpo='Post de teste')
#     meu_post2 = Post(id_usuario=2, titulo='Meu primeiro post no blog', corpo='Post de teste')
#     meu_post3 = Post(id_usuario=3, titulo='Meu primeiro post no blog', corpo='Post de teste')
#     database.session.add(meu_post)
#     database.session.add(meu_post2)
#     database.session.add(meu_post3)
#     database.session.commit()


# =====================================
# # pesquisando posts
# =====================================

# with app.app_context():
#     # buscando na tabela de Post, pegando todos os posts, armazenando na variavel uma lista de posts
#     post = Post.query.all()
#     print(f'\nExibindo a lista de todos os posts: {post}')
#
#     # agora retorna o as informacoes do segundo post
#     post = Post.query[1]
#     # buscando o relacionamento com o usuario para obter dados da tabela usuario atraves da chave estrangeira
#     print(f'\nEncontramos o usuario autor do post, trata-se do: {post.autor}')
#     print(f'\nSegundo post: {post} / id do usuario autor: {post.id_usuario} / email: {post.autor.email}')


# =====================================
# deletando o banco de dados
# =====================================
#
# with app.app_context():
#     database.drop_all()
#     database.create_all()
