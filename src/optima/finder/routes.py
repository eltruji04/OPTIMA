#!/usr/bin/env python3
"""Handles database paths"""

from flask import Blueprint, render_template, request
from .database import (
    search_parts,
)  # Import the search function from the database module

# Create a Blueprint for the Finder module
finder_app = Blueprint(
    "finder",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/finder",
)


@finder_app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the main page of the finder module. Displays a search form
    and, if a search is submitted, displays the search results.

    This route supports both GET and POST methods:
        - GET: Renders the search form.
        - POST: Processes the search query and renders the results.

    Parameters:
        None (handled by Flask)

    Returns:
        str: The HTML content rendered by the 'finder.html' template,
             containing the search results or an empty form.

    Example:
        When a search is performed:
            - A search query is submitted via POST request.
            - The results are fetched from the database and displayed on the page.
    """
    # Initialize an empty list for results
    results = []

    # Process the search query when the form is submitted via POST
    if request.method == "POST":
        # Retrieve the search query from the form
        finder = request.form["finder"]

        # Perform the search and store the results
        results = search_parts(finder)

    # Render the template with the search results
    return render_template("finder.html", results=results)
