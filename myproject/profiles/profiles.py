import secrets
import os
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from myproject import app, db
from myproject.models.forms import FormEditarPerfil

profiles_bp = Blueprint('profiles_bp', __name__, template_folder='templates')

pictures_folder = os.path.join(os.getcwd(), 'static/profile_pictures')


@profiles_bp.route('/perfil')
@login_required
def perfil():
    # definindo a variável que armazenará o caminho da foto de perfil para jogar no HTML
    # current_user significa um objeto de Usuario, onde temos dentro do BD a foto de perfil (string)
    foto_perfil = url_for('static', filename=f'profile_pictures/{current_user.foto_perfil}')
    return render_template('perfilusuario.html', foto_perfil=foto_perfil)


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:  # se o campo estiver marcado, adiciona na lista de cursos
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)  # retornando uma string com os cursos separados por ;


def salvar_imagem(imagem):
    # gera código aleatório de 8bytes para evitar duplicidades de nome de foto no banco de dados
    codigo = secrets.token_hex(8)

    # separa o nome da imagem de sua extensão usando OS, armazena um em cada variável
    nome, extensao = os.path.splitext(imagem.filename)

    # junta novamente o nome da imagem adicionando o código gerado
    nome_arquivo = nome + codigo + extensao

    # define o caminho onde o arquivo será salvo, o app.root_path retorna o caminho do web-blog e o join junta tudo

    caminho_completo = os.path.join(os.getcwd(), 'static/profile_pictures', nome_arquivo)

    # comprime o tamanho da imagem, pois no site é somente 400 por 400, variável tamanho é uma tupla com as dimensões
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    # salva a imagem na pasta static/fotos_perfil
    imagem_reduzida.save(caminho_completo)

    # retorna o novo nome da foto
    return nome_arquivo


@profiles_bp.route('/perfil/editar', methods=['GET', 'POST'])
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

        db.session.commit()
        flash(f'Profile updated successfully!', 'alert-success')
        return redirect(url_for('profiles_bp.perfil'))

    foto_perfil = url_for('static', filename=f'profile_pictures/{current_user.foto_perfil}')

    return render_template('perfileditar.html', foto_perfil=foto_perfil, form=form)
