from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from .database import init_db, get_upcoming_notifications, create_part, get_parts, update_part, delete_part

# Crear un Blueprint para la funcionalidad CRUD
crud_app = Blueprint('crud', __name__, template_folder='templates')

# Inicializar la base de datos (si no existe)
init_db()

# Ruta: Mostrar lista de partes
@crud_app.route('/')
def parts_list():
    """
    Muestra todas las partes almacenadas en la base de datos
    junto con las notificaciones de los recordatorios próximos.
    """
    items = get_parts()
    notifications = get_upcoming_notifications()
    return render_template('parts_list.html', items=items, notifications=notifications)

# Ruta: Crear una nueva parte
@crud_app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        part_number = request.form['part_number']
        item_name = request.form['item_name']
        chapter = int(request.form['chapter'])
        reminder_date = request.form['reminder_date']
        
        # Crear la parte en la base de datos
        create_part(part_number, item_name, chapter, reminder_date)
        return redirect(url_for('crud.parts_list'))

    return render_template('create.html')

# Ruta: Actualizar una parte existente
@crud_app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    if request.method == 'POST':
        part_number = request.form['part_number']
        item_name = request.form['item_name']
        chapter = int(request.form['chapter'])
        reminder_date = request.form['reminder_date']
        
        # Actualizar la parte en la base de datos
        update_part(item_id, part_number, item_name, chapter, reminder_date)
        return redirect(url_for('crud.parts_list'))

    # Obtener los detalles de la parte
    item = get_parts(item_id)
    if not item:
        return f"Item with ID {item_id} not found", 404

    return render_template('update.html', item=item)

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