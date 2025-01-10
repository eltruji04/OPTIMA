from flask import Blueprint, render_template, request
import sqlite3

# Crear el Blueprint (no es necesario 'app' aquí)
buscador_app = Blueprint('buscador', __name__,  template_folder='templates')

# Función para buscar la pieza en la base de datos
def buscar_pieza(busqueda):
    conn = sqlite3.connect('parts.db')
    cursor = conn.cursor()

    # Realizar la búsqueda
    cursor.execute('''
        SELECT * FROM Parts
        WHERE part_number LIKE ? OR item_name LIKE ?
    ''', (f'%{busqueda}%', f'%{busqueda}%'))

    # Obtener los resultados
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@buscador_app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    if request.method == "POST":
        busqueda = request.form["busqueda"]
        resultados = buscar_pieza(busqueda)
    return render_template("index.html", resultados=resultados)
