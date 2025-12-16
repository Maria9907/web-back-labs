from flask import Blueprint, render_template, session, jsonify, request, current_app
import random
from os import path
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3

lab9 = Blueprint('lab9', __name__)

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


def get_all_boxes():
    conn, cur = db_connect()
    try:
        cur.execute("SELECT box_id, is_opened, message, gift_image FROM gift_boxes ORDER BY box_id")
        boxes = cur.fetchall()
        
        boxes_list = []
        for box in boxes:
            boxes_list.append({
                'box_id': box['box_id'],
                'is_opened': box['is_opened'],
                'message': box['message'],
                'gift_image': box['gift_image']
            })
        return boxes_list
    except Exception as e:
        print(f"Ошибка при получении коробок из БД: {e}")
        return []
    finally:
        db_close(conn, cur)

def get_box_by_id(box_id):
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "SELECT box_id, is_opened, message, gift_image FROM gift_boxes WHERE box_id = %s"
        else:
            query = "SELECT box_id, is_opened, message, gift_image FROM gift_boxes WHERE box_id = ?"
        
        cur.execute(query, (box_id,))
        box = cur.fetchone()
        return dict(box) if box else None
    except Exception as e:
        print(f"Ошибка при получении коробки {box_id}: {e}")
        return None
    finally:
        db_close(conn, cur)

def update_box_state(box_id, is_opened):
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "UPDATE gift_boxes SET is_opened = %s WHERE box_id = %s"
        else:
            query = "UPDATE gift_boxes SET is_opened = ? WHERE box_id = ?"
        
        cur.execute(query, (is_opened, box_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при обновлении коробки {box_id}: {e}")
        conn.rollback()
        return False
    finally:
        db_close(conn, cur)

def reset_all_boxes():
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "UPDATE gift_boxes SET is_opened = FALSE"
        else:
            query = "UPDATE gift_boxes SET is_opened = 0"
        
        cur.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при сбросе коробок: {e}")
        conn.rollback()
        return False
    finally:
        db_close(conn, cur)

def count_opened_boxes():
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "SELECT COUNT(*) as count FROM gift_boxes WHERE is_opened = TRUE"
        else:
            query = "SELECT COUNT(*) as count FROM gift_boxes WHERE is_opened = 1"
        
        cur.execute(query)
        result = cur.fetchone()
        return result['count'] if result else 0
    except Exception as e:
        print(f"Ошибка при подсчете открытых коробок: {e}")
        return 0
    finally:
        db_close(conn, cur)


@lab9.route('/lab9/')
def main():
    if 'box_positions' not in session:
        positions = []
        for _ in range(10):
            for _ in range(100):  
                left, top = random.randint(0, 80), random.randint(0, 80)
                if all(abs(left - x) >= 15 or abs(top - y) >= 20 for x, y in positions):
                    positions.append((left, top))
                    break
            else:
                positions.append((left, top))
        session['box_positions'] = positions
    
    if 'opened_count' not in session:
        session['opened_count'] = 0
    
    boxes = get_all_boxes()
    
    total_opened = count_opened_boxes()
    closed_count = 10 - total_opened
    
    return render_template('lab9/index.html', 
                         boxes=boxes,
                         positions=session['box_positions'],
                         closed_count=closed_count,
                         opened_count=session['opened_count'])

@lab9.route('/lab9/rest-api/boxes/', methods=['GET'])
def get_boxes_api():
    """REST API: получить все коробки"""
    boxes = get_all_boxes()
    return jsonify(boxes)

@lab9.route('/lab9/rest-api/boxes/<int:box_id>', methods=['GET'])
def get_box_api(box_id):
    box = get_box_by_id(box_id)
    if not box:
        return jsonify({"error": "Коробка не найдена"}), 404
    return jsonify(box)

@lab9.route('/lab9/rest-api/boxes/<int:box_id>/open', methods=['POST'])
def open_box_api(box_id):
    try:
        # Проверяем валидность ID
        if box_id < 0 or box_id >= 10:
            return jsonify({"error": "Некорректный ID коробки"}), 400
        
        # Получаем коробку из БД
        box = get_box_by_id(box_id)
        if not box:
            return jsonify({"error": "Коробка не найдена"}), 404
        
        # Проверяем, не открыта ли уже
        if box['is_opened']:
            return jsonify({"error": "Эта коробка уже открыта!"}), 400
        
        # Проверяем лимит для пользователя
        if session.get('opened_count', 0) >= 3:
            return jsonify({"error": "Вы уже открыли 3 коробки!"}), 403
        
        # Открываем коробку в БД
        if update_box_state(box_id, True):
            # Обновляем счетчик пользователя
            session['opened_count'] = session.get('opened_count', 0) + 1
            session.modified = True
            
            # Получаем обновленную статистику
            total_opened = count_opened_boxes()
            closed_count = 10 - total_opened
            
            return jsonify({
                "success": True,
                "message": box['message'],
                "gift": box['gift_image'],
                "user_opened_count": session['opened_count'],
                "total_opened_count": total_opened,
                "closed_count": closed_count,
                "box_id": box_id
            })
        else:
            return jsonify({"error": "Ошибка при обновлении БД"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Ошибка: {str(e)}"}), 500

@lab9.route('/lab9/rest-api/boxes/reset', methods=['POST'])
def reset_boxes_api():
    """REST API: сбросить все коробки (Дед Мороз)"""
    # Проверяем авторизацию
    if not session.get('authenticated'):
        return jsonify({"error": "Только для авторизованных пользователей"}), 401
    
    if reset_all_boxes():
        # Сбрасываем счетчик пользователя
        session['opened_count'] = 0
        session.modified = True
        
        return jsonify({
            "success": True,
            "message": "Дед Мороз наполнил все коробки заново! ",
            "closed_count": 10
        })
    else:
        return jsonify({"error": "Ошибка при сбросе коробок"}), 500

@lab9.route('/lab9/rest-api/auth/login', methods=['POST'])
def login_api():
    """REST API: авторизация"""
    data = request.json
    if not data or 'password' not in data:
        return jsonify({"error": "Не указан пароль"}), 400
    
    # Простая проверка пароля
    if data.get('password') == 'secret':
        session['authenticated'] = True
        return jsonify({"success": True, "message": "Вы авторизованы как Дед Мороз "})
    else:
        return jsonify({"error": "Неверный пароль"}), 401

@lab9.route('/lab9/rest-api/auth/logout', methods=['POST'])
def logout_api():
    """REST API: выход"""
    session.pop('authenticated', None)
    return jsonify({"success": True, "message": "Вы вышли из системы"})

@lab9.route('/lab9/rest-api/auth/status', methods=['GET'])
def auth_status_api():
    """REST API: статус авторизации"""
    return jsonify({
        "authenticated": session.get('authenticated', False)
    })