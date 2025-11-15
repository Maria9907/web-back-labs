from flask import Blueprint, redirect, url_for, abort, session, make_response, request, render_template, current_app 
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
lab5 = Blueprint('lab5',__name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'maria_matyushkina_knowledge_base_2',
            user = 'maria_matyushkina_knowledge_base_2',
            password = '123',
            client_encoding='utf8'
        )
        cur = conn.cursor(cursor_factory= RealDictCursor)
    else:
        # Подключение к SQLite
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)  
    return redirect('/lab5/')   

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    full_name = request.form.get('full_name')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    # Проверяем, не существует ли уже пользователь с таким логином
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                               error="Такой пользователь уже существует")
    
    # Хэшируем пароль и создаем нового пользователя
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (%s, %s, %s);", (login, password_hash, full_name))
    else:
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?);", (login, password_hash, full_name))
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

# Авторизация пользователя
@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="заполните поля")
    
    conn, cur = db_connect()

    # Ищем пользователя в базе данных
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    session['login'] = login

    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

# Создание новой статьи
@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))


    if not title or not article_text:
        return render_template('lab5/create_article.html', 
                               error='Название и текст статьи не могут быть пустыми')

    conn, cur = db_connect()


    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        login_id = cur.fetchone()["id"]
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
        login_id = cur.fetchone()["id"]

    
    # Создаем новую статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO articles(login_id, title, article_text, is_favorite, is_public) 
            VALUES (%s, %s, %s, %s, %s);
        """, (login_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("""
            INSERT INTO articles(login_id, title, article_text, is_favorite, is_public) 
            VALUES (?, ?, ?, ?, ?);
        """, (login_id, title, article_text, is_favorite, is_public))
        
    db_close(conn, cur)
    return redirect('/lab5/list')

# Просмотр списка статей пользователя
@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()


    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    login_id = user["id"]

    # Получаем статьи пользователя, отсортированные по избранным и дате
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite DESC, id DESC;", (login_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC, id DESC;", (login_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles, login=login)

# Редактирование статьи
@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.login_id = u.id WHERE a.id=%s;", (article_id,))
    else:
        cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.login_id = u.id WHERE a.id=?;", (article_id,))
    article = cur.fetchone()
    if not article:
        db_close(conn, cur)
        abort(404)

    if article['login'] != login:
        db_close(conn, cur)
        abort(403)
    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)
    

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    
    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', 
                               article=article, 
                               error='Название и текст статьи не могут быть пустыми')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE articles 
            SET title=%s, article_text=%s, is_favorite=%s, is_public=%s 
            WHERE id=%s;
        """, (title, article_text, is_favorite, is_public, article_id))
    else:
        cur.execute("""
            UPDATE articles 
            SET title=?, article_text=?, is_favorite=?, is_public=? 
            WHERE id=?;
        """, (title, article_text, is_favorite, is_public, article_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

# Удаление статьи
@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    # Получаем статью для проверки прав доступа
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.login_id = u.id WHERE a.id=%s;", (article_id,))
    else:
        cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.login_id = u.id WHERE a.id=?;", (article_id,))
    
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        abort(404)

    
    if article['login'] != login:
        db_close(conn, cur)
        abort(403)

    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

# Профиль пользователя
@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)
    
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    full_name = request.form.get('full_name')
    
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    errors = []
    
    
    if new_password:
        if not current_password:
            errors.append('Введите текущий пароль для изменения пароля')
        elif not check_password_hash(user['password'], current_password):
            errors.append('Текущий пароль неверен')
        elif new_password != confirm_password:
            errors.append('Новый пароль и подтверждение не совпадают')
        elif len(new_password) < 3:
            errors.append('Новый пароль слишком короткий')
    
    if errors:
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, errors=errors)
    
    # Обновляем данные пользователя
    if new_password:
        password_hash = generate_password_hash(new_password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET password=%s, full_name=%s WHERE login=%s;", 
                       (password_hash, full_name, login))
        else:
            cur.execute("UPDATE users SET password=?, full_name=? WHERE login=?;", 
                       (password_hash, full_name, login))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET full_name=%s WHERE login=%s;", (full_name, login))
        else:
            cur.execute("UPDATE users SET full_name=? WHERE login=?;", (full_name, login))
    
    db_close(conn, cur)
    return redirect('/lab5/')

# Список всех пользователей
@lab5.route('/lab5/users')
def users_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    # Получаем список всех пользователей
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    
    users = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/users.html', users=users)

# Просмотр публичных статей
@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()
    
    # Получаем все публичные статьи с информацией об авторах
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.*, u.login, u.full_name 
            FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.is_public = TRUE 
            ORDER BY a.is_favorite DESC, a.id DESC;
        """)
    else:
        cur.execute("""
            SELECT a.*, u.login, u.full_name 
            FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.is_public = 1 
            ORDER BY a.is_favorite DESC, a.id DESC;
        """)
    articles = cur.fetchall()
    
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles, login=session.get('login'))
    