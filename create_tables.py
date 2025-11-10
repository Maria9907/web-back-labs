import sqlite3
import os

def create_tables():
   
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute('DROP TABLE IF EXISTS articles;')
    cur.execute('DROP TABLE IF EXISTS users;')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR(30) UNIQUE NOT NULL,
            password VARCHAR(162) NOT NULL,
            full_name VARCHAR(100)
        )
    ''')
    
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login_id INTEGER NOT NULL,
            title VARCHAR(50),
            article_text TEXT,
            is_favorite BOOLEAN DEFAULT 0,
            is_public BOOLEAN DEFAULT 0,
            likes INTEGER DEFAULT 0,
            FOREIGN KEY (login_id) REFERENCES users (id)
        )
    ''')
     # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print("Таблицы успешно созданы!")

if __name__ == '__main__':
    create_tables()