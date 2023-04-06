# os formularios são um objetos dentro do python, uma classe
# no flask já temos formulários prontos, através da biblioteca flask wtf
# para instalar seria flask-wtf e para importar flask_wtf
# temos na bibliteca wtforms os validators, para validarem campos a serem preenchidos pelo usuario

from flask_wtf import FlaskForm  # (install flask-wtf)
# formulário web do flask
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# importando os tipos de campo do wtforms
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# importando validadores de: campo obrigatorio, tamanho, e-mail e comparação de campos (para senha)
# o wtforms não possui o e-mail validator embutido, necessário instalar via terminal: (install email_validator)
from webblog.models import Usuario
# precisaremos da classe usuário para realizar validações nos formulários
from flask_login import current_user
# utilizado na função de validação de e-mail na edição do perfil, pega os atributos do usuário que está logado


class FormCriarConta(FlaskForm):
    # recebe o FlaskForm como herança, ou seja, todas as propriedades dessa classe, não sendo necessário definir init

    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])  # tamanho da senha entre 6 e 20 caract.
    confirmacao = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Criar conta')
    # o parâmetro validators sempre recebe uma lista

    # esse método do FlaskForm se integra ao 'validade_on_submit', ele roda com os demais validators
    # a função tem que começar sempre como 'validate_XXX' para funcionar adequadamente
    @staticmethod
    def validate_email(email):
        usuario = Usuario.query.filter_by(email=email.data).first()  # verificando se usuario tem o mesmo e-mail no BD
        if usuario:  # se retorna algo em usuário, significa duplicidade de email, reportar erro
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')

    @staticmethod
    def validate_username(username):
        usuario = Usuario.query.filter_by(username=username.data).first()  # checando duplicidade de username
        if usuario:  # se retorna algo em usuário, significa duplicidade de username, reportar erro
            raise ValidationError('Usuário já cadastrado. Cadastre-se com outro usuario ou faça login para continuar.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Entrar')  # botoes devem ter nomes diferentes pois estarão na mesma página


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    botao_submit_editar_perfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:  # não permite alteração de email se já existe no BD para outro usuário
            raise ValidationError('Já existe um usuário com esse e-mail. Cadastre um novo e-mail.')
