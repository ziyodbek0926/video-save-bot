import sqlite3
from datetime import datetime

# Ma'lumotlar bazasini yaratish va ulanish
def create_connection():
    conn = sqlite3.connect('bot_stats.db')
    return conn

# Jadval yaratish
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            used_at TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            request_time TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    conn.commit()
    conn.close()

# Foydalanuvchini saqlash funksiyasi
def save_user(user_id, username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, used_at)
        VALUES (?, ?, ?)
    ''', (user_id, username, datetime.now()))
    conn.commit()
    conn.close()

# Foydalanuvchini so'rovlar bilan saqlash
def save_request(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (user_id, request_time)
        VALUES (?, ?)
    ''', (user_id, datetime.now()))
    conn.commit()
    conn.close()

# Statistikani olish
def get_statistics(period):
    conn = create_connection()
    cursor = conn.cursor()

    if period == 'week':
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) FROM requests WHERE request_time > datetime('now', '-7 days')
        ''')
    elif period == 'month':
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) FROM requests WHERE request_time > datetime('now', '-30 days')
        ''')
    else:  # Umumiy so'rovlar soni
        cursor.execute('SELECT COUNT(*) FROM requests')

    count = cursor.fetchone()[0]
    conn.close()
    return count
