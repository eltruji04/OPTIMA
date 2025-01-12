from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

# Create a Blueprint for the CRUD functionality
crud_app = Blueprint('crud', __name__, template_folder='templates',)

# Database Initialization
def init_db():
    """
    Initializes the database by creating the 'items' table if it doesn't exist.

    The table contains the following columns:
    - id: INTEGER, Primary Key, Auto Increment
    - part_number: TEXT, Not Null
    - item_name: TEXT, Not Null
    - chapter: INTEGER, Not Null
    - reminder_date: TEXT (Date in 'YYYY-MM-DD' format)
    - notification_shown: INTEGER, Default 0 (Flag to check if notification has been shown)

    This function is typically called at the application's startup.
    """
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_number TEXT NOT NULL,
                item_name TEXT NOT NULL,
                chapter INTEGER NOT NULL,
                reminder_date TEXT,
                notification_shown INTEGER DEFAULT 0
            )
        ''')
    print("Database initialized")

# Notification Functionality
def get_upcoming_notifications():
    notifications = []
    today = datetime.now().date()

    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, item_name, reminder_date 
            FROM items 
            WHERE reminder_date IS NOT NULL AND notification_shown = 0
        ''')
        items = cursor.fetchall()

        for item_id, item_name, reminder_date in items:
            reminder_date = datetime.strptime(reminder_date, '%Y-%m-%d').date()
            if today == reminder_date - timedelta(days=1):  # One day before
                notifications.append({
                    'item_name': item_name,
                    'message': f"Tomorrow is the reminder date for '{item_name}'."
                })
            elif today == reminder_date:  # Same day
                notifications.append({
                    'item_name': item_name,
                    'message': f"Today is the reminder date for '{item_name}'."
                })

    return notifications

# Route: Display list of parts
@crud_app.route('/')
def parts_list():
    """
    Displays all parts stored in the database along with any notifications for upcoming reminders.
    """
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()

    notifications = get_upcoming_notifications()
    return render_template('parts_list.html', items=items, notifications=notifications)

# Route: Create a new part
@crud_app.route('/create', methods=['GET', 'POST'])
def create():
    """
    Handles the creation of a new part. If the request is GET, renders the creation form.
    If the request is POST, inserts the new part into the database.
    """
    if request.method == 'POST':
        part_number = request.form['part_number']
        item_name = request.form['item_name']
        chapter = int(request.form['chapter'])
        reminder_date = request.form['reminder_date']

        with sqlite3.connect('active_parts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO items (part_number, item_name, chapter, reminder_date) 
                VALUES (?, ?, ?, ?)
            ''', (part_number, item_name, chapter, reminder_date))
            conn.commit()
        return redirect(url_for('crud.parts_list'))

    return render_template('create.html')

# Route: Update an existing part
@crud_app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    """
    Updates an existing part record. If the request is GET, retrieves the current 
    part information and pre-fills the update form. If the request is POST, updates 
    the record in the database.
    """
    if request.method == 'POST':
        part_number = request.form['part_number']
        item_name = request.form['item_name']
        chapter = int(request.form['chapter'])
        reminder_date = request.form['reminder_date']

        with sqlite3.connect('active_parts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE items 
                SET part_number = ?, item_name = ?, chapter = ?, reminder_date = ?, notification_shown = 0 
                WHERE id = ?
            ''', (part_number, item_name, chapter, reminder_date, item_id))
            conn.commit()
        return redirect(url_for('crud.parts_list'))

    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = cursor.fetchone()

    if not item:
        return f"Item with ID {item_id} not found", 404

    return render_template('update.html', item={
        'id': item[0],
        'part_number': item[1],
        'item_name': item[2],
        'chapter': item[3],
        'reminder_date': item[4],
    })

# Route: Delete a part
@crud_app.route('/delete/<int:item_id>', methods=['GET', 'POST'])
def delete(item_id):
    """
    Deletes a part from the database based on its ID.
    """
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()
    return redirect(url_for('crud.parts_list'))
