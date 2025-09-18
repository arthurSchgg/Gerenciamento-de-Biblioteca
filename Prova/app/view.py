from app import app, db
from flask import render_template, redirect, url_for, flash, request, abort
from app.forms import LoginForm, TurmaForm, AtividadeForm, CadastroProfessorForm
from app.models import Professor, Turma, Atividade
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroProfessorForm()
    if form.validate_on_submit():
        from werkzeug.security import generate_password_hash
        novo_professor = Professor(
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(novo_professor)
        try:
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar: ' + str(e), 'danger')
    return render_template('cadastro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        professor = Professor.query.filter_by(username=form.username.data).first()
        if professor and check_password_hash(professor.password_hash, form.password.data):
            login_user(professor)
            return redirect(url_for('lista_turmas'))  
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('login'))

@app.route('/lista_turmas')
@login_required
def lista_turmas():  
    turmas = current_user.turmas
    return render_template('lista_turmas.html', turmas=turmas)

@app.route('/turma/criar', methods=['GET', 'POST'])
@login_required
def criar_turma():
    form = TurmaForm()
    if form.validate_on_submit():
        nova_turma = Turma(nome=form.nome.data, professor=current_user)
        db.session.add(nova_turma)
        try:
            db.session.commit()
            flash('Turma criada com sucesso!', 'success')
            return redirect(url_for('lista_turmas'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar turma: ' + str(e), 'danger')
    return render_template('criar_turma.html', form=form)

@app.route('/turma/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_turma(id):
    turma = Turma.query.get_or_404(id)
    if turma.professor_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('lista_turmas'))
    db.session.delete(turma)
    try:
        db.session.commit()
        flash('Turma excluída.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir turma: ' + str(e), 'danger')
    return redirect(url_for('lista_turmas'))

@app.route('/turma/<int:id>')
@login_required
def ver_turma(id):
    turma = Turma.query.get_or_404(id)
    if turma.professor_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('lista_turmas'))
    atividades = turma.atividades
    return render_template('ver_turma.html', turma=turma, atividades=atividades)

@app.route('/turma/<int:id>/atividade/criar', methods=['GET', 'POST'])
@login_required
def criar_atividade(id):
    turma = Turma.query.get_or_404(id)
    if turma.professor_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('lista_turmas'))
    form = AtividadeForm()
    if form.validate_on_submit():
        atividade = Atividade(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            turma=turma
        )
        db.session.add(atividade)
        try:
            db.session.commit()
            flash('Atividade criada com sucesso!', 'success')
            return redirect(url_for('ver_turma', id=id))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar atividade: ' + str(e), 'danger')
    return render_template('criar_atividade.html', form=form, turma=turma)
