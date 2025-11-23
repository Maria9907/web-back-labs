from flask import Blueprint, redirect, url_for, abort, session, make_response, request, render_template, current_app 
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path


lab6 = Blueprint('lab6',__name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='maria_matyushkina_knowledge_base_2',
            user='maria_matyushkina_knowledge_base_2',
            password='123',
            client_encoding='utf8'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
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



@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        conn, cur = db_connect()
        
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
            else:
                cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
            
            offices_data = cur.fetchall()
            
            
            offices_list = []
            for office in offices_data:
                if current_app.config['DB_TYPE'] == 'postgres':
                    offices_list.append({
                        'number': office['number'],
                        'tenant': office['tenant'],
                        'price': office['price']
                    })
                else:
                    offices_list.append({
                        'number': office[0],
                        'tenant': office[1],
                        'price': office[2]
                    })
            
            return {
                'jsonrpc': '2.0',
                'result': offices_list,
                'id': id
            }
        finally:
            db_close(conn, cur)
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()
        
        try:
            # Проверяем существование офиса
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM offices WHERE number=%s;", (office_number,))
            else:
                cur.execute("SELECT * FROM offices WHERE number=?;", (office_number,))
            
            office = cur.fetchone()
            
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Office not found'
                    },
                    'id': id
                }
            
            # Проверяем, занят ли офис
            tenant = office['tenant'] if current_app.config['DB_TYPE'] == 'postgres' else office[1]
            if tenant:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Already booked'
                    },
                    'id': id
                }
            
            # Бронируем офис
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE offices SET tenant=%s WHERE number=%s;", (login, office_number))
            else:
                cur.execute("UPDATE offices SET tenant=? WHERE number=?;", (login, office_number))
            
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        finally:
            db_close(conn, cur)
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        conn, cur = db_connect()
        
        try:
            # Проверяем существование офиса
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM offices WHERE number=%s;", (office_number,))
            else:
                cur.execute("SELECT * FROM offices WHERE number=?;", (office_number,))
            
            office = cur.fetchone()
            
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Office not found'
                    },
                    'id': id
                }
            
            # Проверяем, арендован ли офис
            tenant = office['tenant'] if current_app.config['DB_TYPE'] == 'postgres' else office[1]
            if not tenant:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 4,
                        'message': 'Office is not booked'
                    },
                    'id': id
                }
            
            # Проверяем, что офис арендован текущим пользователем
            if tenant != login:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'You are not the tenant of this office'
                    },
                    'id': id
                }
            
            # Снимаем аренду
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE offices SET tenant='' WHERE number=%s;", (office_number,))
            else:
                cur.execute("UPDATE offices SET tenant='' WHERE number=?;", (office_number,))
            
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        finally:
            db_close(conn, cur)

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }