from flask import Blueprint, render_template, request
import sqlite3

# Create a Blueprint for the finder module
# This Blueprint handles searching for parts in the database
finder_app = Blueprint('finder', __name__, template_folder='templates')

def parts_finder(finder):
    """
    Searches for parts in the database that match the given query.

    Parameters:
        finder (str): The search term used to find matching parts 
        in the database.

    Returns:
        list: A list of tuples representing rows from the 
        Parts table that match the search term.
    """
    # Connect to the database
    conn = sqlite3.connect('parts.db')
    cursor = conn.cursor()

    # Perform the search in the database
    cursor.execute('''
        SELECT * FROM Parts
        WHERE part_number LIKE ? OR item_name LIKE ?
    ''', (f'%{finder}%', f'%{finder}%'))

    # Fetch all matching rows
    results = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Return the search results
    return results

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
        results = parts_finder(finder)

    # Render the template with the search results
    return render_template("index.html", results=results)
