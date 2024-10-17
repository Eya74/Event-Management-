from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

def init_db():
    conn = sqlite3.connect('events.db')
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

def validate_event(name, date):
    errors = []
    if not name or len(name) < 3:
        errors.append("Event name must be at least 3 characters long.")
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        errors.append("Invalid date format. Please use YYYY-MM-DD.")
    return errors

@app.route('/')
def home():
    try:
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
        conn.close()
        return render_template('index.html', events=events)
    except sqlite3.Error as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('index.html', events=[])

@app.route('/create_event')
def create_event():
    return render_template('event_form.html')

@app.route('/submit_event', methods=['POST'])
def submit_event():
    name = request.form['name']
    date = request.form['date']
    
    errors = validate_event(name, date)
    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template('event_form.html', name=name, date=date)
    
    try:
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO events (name, date) VALUES (?, ?)', (name, date))
        conn.commit()
        conn.close()
        flash('Event created successfully!', 'success')
        return redirect(url_for('home'))
    except sqlite3.Error as e:
        flash(f"An error occurred while creating the event: {str(e)}", 'error')
        return render_template('event_form.html', name=name, date=date)

@app.route('/delete_event/<int:id>', methods=['POST'])
def delete_event(id):
    try:
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM events WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Event deleted successfully!', 'success')
    except sqlite3.Error as e:
        flash(f"An error occurred while deleting the event: {str(e)}", 'error')
    return redirect(url_for('home'))

@app.route('/edit_event/<int:id>')
def edit_event(id):
    try:
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events WHERE id = ?', (id,))
        event = cursor.fetchone()
        conn.close()
        if event:
            return render_template('edit_event.html', event=event)
        else:
            flash('Event not found.', 'error')
            return redirect(url_for('home'))
    except sqlite3.Error as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('home'))

@app.route('/update_event/<int:id>', methods=['POST'])
def update_event(id):
    name = request.form['name']
    date = request.form['date']
    
    errors = validate_event(name, date)
    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template('edit_event.html', event=(id, name, date))
    
    try:
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE events SET name = ?, date = ? WHERE id = ?', (name, date, id))
        conn.commit()
        conn.close()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('home'))
    except sqlite3.Error as e:
        flash(f"An error occurred while updating the event: {str(e)}", 'error')
        return render_template('edit_event.html', event=(id, name, date))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)