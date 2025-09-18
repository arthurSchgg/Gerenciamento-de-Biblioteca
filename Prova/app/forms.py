from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import Professor

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class TurmaForm(FlaskForm):
    nome = StringField('Nome da Turma', validators=[DataRequired(), Length(min=2, max=150)])
    submit = SubmitField('Salvar Turma')

class AtividadeForm(FlaskForm):
    titulo = StringField('Título da Atividade', validators=[DataRequired(), Length(min=2, max=150)])
    descricao = TextAreaField('Descrição')
    submit = SubmitField('Salvar Atividade')

class CadastroProfessorForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password', message='Senhas devem ser iguais.')])
    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        usuario = Professor.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Este usuário já existe. Escolha outro nome.')