from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')

DATABASE_URL = 'events.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO events (name, date, description) VALUES (?, ?, ?)',
                       (name, date, description))
        conn.commit()
        conn.close()
        flash('Event created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('event_form.html', event=None)

@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        
        cursor.execute('UPDATE events SET name = ?, date = ?, description = ? WHERE id = ?',
                       (name, date, description, id))
        conn.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('home'))
    
    cursor.execute('SELECT * FROM events WHERE id = ?', (id,))
    event = cursor.fetchone()
    conn.close()
    
    if event is None:
        flash('Event not found.', 'error')
        return redirect(url_for('home'))
    
    return render_template('event_form.html', event=event)

@app.route('/delete_event/<int:id>', methods=['POST'])
def delete_event(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)