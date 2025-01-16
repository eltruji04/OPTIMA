from flask import Flask, render_template
# Import the parts finder Blueprint
from parts_finder.parts_finder import finder_app
# Import the CRUD Blueprint
from CRUD.crud import crud_app

# Initialize the Flask application
app = Flask(__name__, static_folder='manuals')
# static_folder='manuals'
# indicates the directory where static files like PDFs are stored.

# Route for the main entry point of the application
@app.route('/')
def index():
    """
    Render the main page of the application.
    This serves as the homepage and provides links to 
    access different features.
    """
    return render_template('main-page.html')

# Register the parts finder Blueprint with the URL prefix '/finder'
app.register_blueprint(finder_app, url_prefix='/finder')

# Register the CRUD Blueprint with the URL prefix '/crud'
app.register_blueprint(crud_app, url_prefix='/crud')

if __name__ == '__main__':
    # Run the application in debug mode to enable
    # live reloading and detailed error messages
    # during development
    app.run(debug=True)
