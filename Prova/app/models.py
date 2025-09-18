from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import pytz
 

@login_manager.user_loader
def load_user(user_id):
    return Professor.query.get(int(user_id))

class Professor(UserMixin, db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    turmas = db.relationship('Turma', backref='professor', lazy=True)

    def __repr__(self):
        return f'<Professor {self.username}>'

class Turma(db.Model):
    __tablename__ = 'turmas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    atividades = db.relationship('Atividade', backref='turma', lazy=True)

    def __repr__(self):
        return f'<Turma {self.nome}>'

class Atividade(db.Model):
    __tablename__ = 'atividades'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    
@property
def data_local(self):
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    if self.data_criacao is not None:
        if self.data_criacao.tzinfo is None:
            utc = pytz.utc
            data_utc = utc.localize(self.data_criacao)
        else:
            data_utc = self.data_criacao
            return data_utc.astimezone(fuso_brasil)
        return None

    def __repr__(self):
        return f'<Atividade {self.titulo}>'
