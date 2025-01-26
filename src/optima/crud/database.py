import sqlite3
from datetime import datetime, timedelta

# Inicialización de la base de datos
def init_db():
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

# Función para obtener las notificaciones próximas
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
            if reminder_date:
                reminder_date = datetime.strptime(reminder_date, '%Y-%m-%d').date()
                if today == reminder_date - timedelta(days=1):
                    notifications.append({
                        'item_name': item_name,
                        'message': f"Tomorrow is the reminder date for '{item_name}'."
                    })
                elif today == reminder_date:
                    notifications.append({
                        'item_name': item_name,
                        'message': f"Today is the reminder date for '{item_name}'."
                    })

    return notifications

# Función para crear una nueva parte
def create_part(part_number, item_name, chapter, reminder_date):
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO items (part_number, item_name, chapter, reminder_date) 
            VALUES (?, ?, ?, ?)
        ''', (part_number, item_name, chapter, reminder_date))
        conn.commit()

# Función para obtener todas las partes
def get_parts(item_id=None):
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        if item_id:
            cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            item = cursor.fetchone()
            return item
        else:
            cursor.execute('SELECT * FROM items')
            items = cursor.fetchall()
            return items

# Función para actualizar una parte existente
def update_part(item_id, part_number, item_name, chapter, reminder_date):
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE items 
            SET part_number = ?, item_name = ?, chapter = ?, reminder_date = ?, notification_shown = 0 
            WHERE id = ?
        ''', (part_number, item_name, chapter, reminder_date, item_id))
        conn.commit()

# Función para eliminar una parte
def delete_part(item_id):
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()