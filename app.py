import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Handle potential "postgres://" style URLs for Railway
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
else:
    database_url = 'sqlite:///events.db'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy after all configurations are set
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)

# Ensure all routes are registered before running create_all()
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        
        new_event = Event(name=name, date=date, description=description)
        try:
            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}', 'error')
        return redirect(url_for('home'))
    return render_template('event_form.html', event=None)

@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    event = Event.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            event.name = request.form['name']
            event.date = request.form['date']
            event.description = request.form['description']
            db.session.commit()
            flash('Event updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating event: {str(e)}', 'error')
        return redirect(url_for('home'))
    
    return render_template('event_form.html', event=event)

@app.route('/delete_event/<int:id>', methods=['POST'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'error')
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)