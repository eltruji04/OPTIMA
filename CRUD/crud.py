from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Crear el Blueprint
crud_app = Blueprint('crud', __name__, template_folder='templates')

# Función para inicializar la base de datos
def init_db():
    with sqlite3.connect('piezas_activas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_number TEXT NOT NULL,
                item_name TEXT NOT NULL,
                chapter INTEGER NOT NULL
            )
        ''')
    print("Base de datos inicializada")

# Ruta para mostrar las piezas
@crud_app.route('/')
def parts_list():
    with sqlite3.connect('piezas_activas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
    return render_template('parts_list.html', items=items)

# Ruta para crear un nuevo registro
@crud_app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        part_number = request.form['part_number']
        item_name = request.form['item_name']
        chapter = int(request.form['chapter'])

        with sqlite3.connect('piezas_activas.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO items (part_number, item_name, chapter) VALUES (?, ?, ?)', 
                           (part_number, item_name, chapter))
            conn.commit()
        return redirect(url_for('crud.parts_list'))
    return render_template('create.html')

# Ruta para actualizar un registro
@crud_app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    if request.method == 'POST':
        part_number = request.form['part_number']
        item_name = request.form['item_name']
        chapter = int(request.form['chapter'])

        with sqlite3.connect('piezas_activas.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE items SET part_number = ?, item_name = ?, chapter = ? WHERE id = ?', 
                           (part_number, item_name, chapter, item_id))
            conn.commit()
        return redirect(url_for('crud.parts_list'))

    with sqlite3.connect('piezas_activas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = cursor.fetchone()
    return render_template('update.html', item=item)

# Ruta para eliminar un registro
@crud_app.route('/delete/<int:item_id>', methods=['GET', 'POST'])
def delete(item_id):
    with sqlite3.connect('piezas_activas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()
    return redirect(url_for('crud.parts_list'))
