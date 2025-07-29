import sqlite3

with sqlite3.connect("local.db") as conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        number TEXT,
        dob TEXT,
        password TEXT,
        location TEXT,
        cookie TEXT,
        accessToken TEXT,
        lastLogin TEXT,
        last_pw_change TEXT,
        accountCreationDateTime TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        thread_id TEXT,
        sender_id TEXT,
        sender_name TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_groups (
         user_id TEXT,
         group_id TEXT
     )''')
