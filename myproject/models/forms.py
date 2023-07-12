from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .class_usuario import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):

    username = StringField('User name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Create account')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail already registered. Sign-up with another e-mail or Sign-in to continue.')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()  # checando duplicidade de username
        if usuario:  # se retorna algo em usuário, significa duplicidade de username, reportar erro
            raise ValidationError('Username already registered. Sign-up with another username or Sign-in to continue.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Remember me')
    botao_submit_login = SubmitField('Log in')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()  # verificando se o e-mail existe no BD
        if not usuario:  # se não retornar, informa que não existe usuário com esse e-mail
            raise ValidationError('There is no username linked to this e-mail. Try again or Sign-up for free.')


class FormEditarPerfil(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    curso_excel = BooleanField('Excel')
    curso_vba = BooleanField('VBA')
    curso_powerbi = BooleanField('Power BI')
    curso_python = BooleanField('Python')
    curso_ppt = BooleanField('Power Point')
    curso_sql = BooleanField('SQL')
    botao_submit_editar_perfil = SubmitField('Update Profile')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:  # não permite alteração de email se já existe no BD para outro usuário
                raise ValidationError('This e-mail is already being used. Please register a different e-mail.')


    def validate_username(self, username):
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:  # não permite alteração de email se já existe no BD para outro usuário
                raise ValidationError('This username is already being used. Please register a different username.')


class FormCriarPost(FlaskForm):
    titulo = StringField('Post Title', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Post Content', validators=[DataRequired()])
    botao_submit = SubmitField('Create Post')


class FormEditarPost(FlaskForm):
    titulo = StringField('Post Title', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Post Content', validators=[DataRequired()])
    botao_submit = SubmitField('Edit Post')
