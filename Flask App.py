# app.py

import os
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')

# Use DATABASE_URL environment variable for database connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///events.db')

def get_db_connection():
    if DATABASE_URL.startswith('sqlite:///'):
        return sqlite3.connect(DATABASE_URL.replace('sqlite:///', ''))
    else:
        # For other databases (e.g., PostgreSQL), you'd use a different connection method
        # This example assumes SQLite, but you'd need to modify this for other databases
        raise NotImplementedError("Only SQLite is supported in this example")

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# ... (rest of the functions remain the same) ...

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)