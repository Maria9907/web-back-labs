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

    login_user(new_user)
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

    if user and check_password_hash(user.password, password_form):
        # ИСПРАВЛЕНО: используем login_user() из Flask-Login
        login_user(user, remember=remember_me)
        return redirect('/lab8/')
        
    return render_template('lab8/login.html',
                               error='Логин и/или пароль неверны')



@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')






# Создание статьи
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required  # Flask-Login защищает маршрут
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    # Получаем данные из формы
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))
    
    # Проверка на пустые значения
    if not title:
        return render_template('lab8/create_article.html', 
                               error='Название статьи не может быть пустым',
                               title=title, article_text=article_text,
                               is_favorite=is_favorite, is_public=is_public)
    
    if not article_text:
        return render_template('lab8/create_article.html', 
                               error='Текст статьи не может быть пустым',
                               title=title, article_text=article_text,
                               is_favorite=is_favorite, is_public=is_public)
    
    # Создаем новую статью
    new_article = articles(
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public,
        login_id=current_user.id
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles')

# Редактирование статьи
@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required  # Flask-Login защищает маршрут
def edit_article(article_id):
    # Получаем статью текущего пользователя
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        return "Статья не найдена или у вас нет прав на её редактирование", 404
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    # Обработка POST запроса
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))
    
    if not title:
        return render_template('lab8/edit_article.html', 
                               article=article,
                               error='Название статьи не может быть пустым')
    
    if not article_text:
        return render_template('lab8/edit_article.html', 
                               article=article,
                               error='Текст статьи не может быть пустым')
    
    # Обновляем статью
    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public
    
    db.session.commit()
    
    return redirect('/lab8/articles')

# Удаление статьи
@lab8.route('/lab8/delete/<int:article_id>')
@login_required  # Flask-Login защищает маршрут
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if article:
        db.session.delete(article)
        db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/public')
def public_articles():
    query = request.args.get('query', '').strip().lower()
    
    # Получаем все публичные статьи
    base_query = articles.query.filter_by(is_public=True)
    
    # Если есть поисковый запрос
    if query:
        articles_list = []
        all_public_articles = base_query.all()
        
        for article in all_public_articles:
            title_lower = article.title.lower() if article.title else ""
            text_lower = article.article_text.lower() if article.article_text else ""
            
            if query in title_lower or query in text_lower:
                articles_list.append(article)
    else:
        articles_list = base_query.all()
    
    return render_template('lab8/public_articles.html', 
                          articles=articles_list, 
                          query=query)


@lab8.route('/lab8/articles')
@login_required
def article_list():
    query = request.args.get('query', '').strip().lower()
    
    # Для авторизованного пользователя показываем публичные + свои статьи
    base_query = articles.query.filter(
        (articles.is_public == True) | (articles.login_id == current_user.id)
    )
    
    # Если есть поисковый запрос
    if query:
        articles_list = []
        all_articles = base_query.all()
        
        for article in all_articles:
            title_lower = article.title.lower() if article.title else ""
            text_lower = article.article_text.lower() if article.article_text else ""
            
            if query in title_lower or query in text_lower:
                articles_list.append(article)
    else:
        articles_list = base_query.all()
    
    return render_template('lab8/articles.html', 
                          articles=articles_list, 
                          query=query)