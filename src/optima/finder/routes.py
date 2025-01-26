from flask import Blueprint, render_template, request
from .database import search_parts  # Importa la función desde el módulo de la base de datos

# Crea un Blueprint para el módulo Finder
finder_app = Blueprint('finder', __name__, template_folder='templates')

@finder_app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the main page of the finder module. Displays a search form
    and, if a search is submitted, displays the search results.

    Methods:
        GET: Renders the search form.
        POST: Processes the search query and renders the results.

    Returns:
        str: The HTML content rendered by the template.
    """
    results = []  # Initialize an empty list for results

    if request.method == "POST":
        # Retrieve the search query from the form
        finder = request.form["finder"]

        # Perform the search
        results = search_parts(finder)

    # Render the template with the search results
    return render_template("finder.html", results=results)
