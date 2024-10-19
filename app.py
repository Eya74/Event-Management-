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
        date TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def validate_event(name, date, description):
    errors = []
    if not name or len(name) < 3:
        errors.append("Event name must be at least 3 characters long.")
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        errors.append("Invalid date format. Please use YYYY-MM-DD.")
    if not description or len(description) < 5:
        errors.append("Event description must be at least 5 characters long.")
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

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        
        errors = validate_event(name, date, description)
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('event_form.html', name=name, date=date, description=description)
        
        try:
            conn = sqlite3.connect('events.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO events (name, date, description) VALUES (?, ?, ?)', (name, date, description))
            conn.commit()
            conn.close()
            flash('Event created successfully!', 'success')
            return redirect(url_for('home'))
        except sqlite3.Error as e:
            flash(f"An error occurred while creating the event: {str(e)}", 'error')
            return render_template('event_form.html', name=name, date=date, description=description)
    
    return render_template('event_form.html')

@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        
        errors = validate_event(name, date, description)
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('edit_event.html', event={'id': id, 'name': name, 'date': date, 'description': description})
        
        try:
            conn = sqlite3.connect('events.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE events SET name = ?, date = ?, description = ? WHERE id = ?', (name, date, description, id))
            conn.commit()
            conn.close()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('home'))
        except sqlite3.Error as e:
            flash(f"An error occurred while updating the event: {str(e)}", 'error')
            return render_template('edit_event.html', event={'id': id, 'name': name, 'date': date, 'description': description})
    
    try:
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events WHERE id = ?', (id,))
        event = cursor.fetchone()
        conn.close()
        if event:
            return render_template('edit_event.html', event={'id': event[0], 'name': event[1], 'date': event[2], 'description': event[3]})
        else:
            flash('Event not found.', 'error')
            return redirect(url_for('home'))
    except sqlite3.Error as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('home'))

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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)