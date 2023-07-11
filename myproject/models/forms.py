from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .class_usuario import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):

    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()  # checando duplicidade de username
        if usuario:  # se retorna algo em usuário, significa duplicidade de username, reportar erro
            raise ValidationError('Usuário já cadastrado. Cadastre-se com outro usuario ou faça login para continuar.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Entrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()  # verificando se o e-mail existe no BD
        if not usuario:  # se não retornar, informa que não existe usuário com esse e-mail
            raise ValidationError('Não existe usuário vinculado ao e-mail informado. Tente novamente ou cadastre-se.')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Alterar foto do perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    curso_excel = BooleanField('Excel')
    curso_vba = BooleanField('VBA')
    curso_powerbi = BooleanField('Power BI')
    curso_python = BooleanField('Python')
    curso_ppt = BooleanField('Power Point')
    curso_sql = BooleanField('SQL')
    botao_submit_editar_perfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:  # não permite alteração de email se já existe no BD para outro usuário
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre um novo e-mail.')


    def validate_username(self, username):
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:  # não permite alteração de email se já existe no BD para outro usuário
                raise ValidationError('Já existe um usuário com esse username. Cadastre um novo username.')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')


class FormEditarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Conteúdo do Post', validators=[DataRequired()])
    botao_submit = SubmitField('Editar Post')
