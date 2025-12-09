from flask import Blueprint, render_template, request, abort, jsonify, current_app, redirect
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from db import db
from db.models import users,articles
lab8 = Blueprint('lab8', __name__)




@lab8.route('/lab8/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login').strip()
    password_form = request.form.get('password').strip()

    errors = []
    
    if not login_form:
        errors.append('Имя пользователя не может быть пустым')
    
    if not password_form:
        errors.append('Пароль не может быть пустым')
    
    if errors:
        return render_template('lab8/register.html',
                               errors=errors)
    
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')


