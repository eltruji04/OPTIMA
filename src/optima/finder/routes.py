#!/usr/bin/env python3
"""Handles database search functionality for the Finder module."""

from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from functools import wraps

# Import the search function from the database module
from .database import search_parts


# Create a Blueprint for the Finder module
finder_app = Blueprint(
    "finder",
    __name__,
    template_folder="templates",  # Templates folder
    static_folder="static",       # Static files folder
)


# Helper function to check if the user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You must log in to access this page.", "danger")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated_function


# Decorator to restrict access based on user role
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("role") != role:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("login.login"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Route: Main Page of the Finder Module
@finder_app.route("/", methods=["GET", "POST"])
@login_required
@role_required("admin")  # Solo los administradores pueden acceder
def index():
    """
    Handles the main page of the Finder module.

    This route supports both GET and POST methods:
        - GET: Renders the search form.
        - POST: Processes the search query and displays the results.

    Returns:
        str: The HTML content rendered by the 'admin_finder.html' template,
             containing either the search results or an empty form.

    Example:
        When a search is performed:
            - A search query is submitted via POST request.
            - The results are fetched from the database and displayed on the page.
    """
    # Initialize an empty list for results
    results = []

    # Process the search query when the form is submitted via POST
    if request.method == "POST":
        try:
            # Retrieve the search query from the form
            finder = request.form.get("finder", "").strip()

            # Validate the search query
            if not finder:
                return render_template(
                    "admin_finder.html",
                    error="The search field cannot be empty."
                )

            # Perform the search and store the results
            results = search_parts(finder)

            # If no results are found, display a message
            if not results:
                return render_template(
                    "admin_finder.html",
                    error="No results found for your search."
                )

        except Exception as e:
            # Log the error and return a user-friendly message
            print(f"Error during search: {e}")
            return render_template(
                "admin_finder.html",
                error="An error occurred during the search. Please try again."
            )

    # Render the template with the search results
    return render_template("admin_finder.html", results=results)
