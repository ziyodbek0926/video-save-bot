import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        last_request_time TIMESTAMP
    )
''')
conn.commit()

# Save user information and update their last request time
def save_user(user_id, username):
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, last_request_time)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (user_id, username))
    conn.commit()

# Get user by ID
def get_user(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

# Count users who have made requests within a time range (e.g., last week, last month)
def count_users_in_time_range(time_range):
    cursor.execute(f'''
        SELECT COUNT(DISTINCT user_id) FROM users
        WHERE last_request_time >= datetime('now', '-{time_range}')
    ''')
    return cursor.fetchone()[0]

# Count the total number of requests made in the system
def count_total_requests():
    cursor.execute('SELECT COUNT(*) FROM users')
    return cursor.fetchone()[0]

# Close the connection to the database
def close_connection():
    conn.close()

# Remove user data after sending the content
def remove_user_data(user_id):
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
