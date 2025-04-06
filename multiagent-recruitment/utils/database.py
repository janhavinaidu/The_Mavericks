# utils/database.py
import os
import sqlite3

# Ensure 'database/' folder exists
os.makedirs('database', exist_ok=True)

DB_NAME = 'database/recruitment.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortlisted (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            match_score INTEGER,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_candidate(name, email, score, reason):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO shortlisted (name, email, match_score, reason)
        VALUES (?, ?, ?, ?)
    ''', (name, email, score, reason))
    conn.commit()
    conn.close()
