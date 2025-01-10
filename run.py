from flask import Flask, render_template
from buscador_piezas.buscador_piezas import buscador_app  # Importa el Blueprint correctamente
from CRUD.crud import crud_app  # Importa el Blueprint correctamente

# Crear la app principal
app = Flask(__name__, static_folder='manuals')

# Ruta principal que sirve pagina-principal.html
@app.route('/')
def index():
    return render_template('pagina-principal.html')

# Incluye las rutas de los Blueprints
app.register_blueprint(buscador_app, url_prefix='/buscador')
app.register_blueprint(crud_app, url_prefix='/crud')

if __name__ == "__main__":
    app.run(debug=True)
