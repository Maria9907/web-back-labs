from flask import Blueprint, render_template, request, abort, jsonify, current_app, redirect,session
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from db import db
from db.models import users,articles
from flask_login import login_user, login_required, current_user, logout_user
lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    if 'login' in session:
        user_login = session['login']
        user = users.query.filter_by(login=user_login).first()
        return render_template('lab8/lab8.html', login=user_login, user=user)
    else:
        return render_template('lab8/lab8.html')


@lab8.route('/lab8/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()

    
    if not login_form:
        return render_template('lab8/register.html',
                               error='Имя пользователя не может быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html',
                               error='Пароль не может быть пустым')
    
    
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    session['login'] = login_form

    return redirect('/lab8/')


@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()
    remember_me = request.form.get('remember') == 'true'  # Проверяем галочку

    if not login_form:
        return render_template('lab8/login.html',
                               error='Логин не может быть пустым')
    
    if not password_form:
        return render_template('lab8/login.html',
                               error='Пароль не может быть пустым')


    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            session['login'] = login_form
            if remember_me:
                session.permanent = True  # Делаем сессию постоянной
            else:
                session.permanent = False  # Сессия только для текущей сессии браузера

            return redirect('/lab8/')
        
    return render_template('lab8/login.html',
                               error='Логин и/или пароль неверны')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "список статей"

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')