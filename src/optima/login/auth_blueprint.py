#!/usr/bin/env python3
"""Blueprint for handling authentication-related routes."""

from flask import Blueprint, render_template, request, redirect, url_for, flash

# Import authentication functions
from .auth_functions import login_user, register_user, logout_user


# Create a Blueprint for authentication routes
login_bp = Blueprint(
    "login",
    __name__,
    template_folder="templates",  # Templates folder
    static_folder="static",       # Static files folder
)


@login_bp.route("/", methods=["GET", "POST"])
def login():
    """
    Handles the login page.

    Displays the login form and processes user login attempts.

    Returns:
        str: The HTML content rendered by the appropriate template based on the user's role.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Authenticate the user
        user = login_user(username, password)
        if user:
            role = user["role"]

            # Redirect based on the user's role
            if role == "user":
                return redirect(url_for("login.home_user"))
            elif role == "admin":
                return redirect(url_for("login.admin_dashboard"))
            else:
                flash("Unknown role. Please contact the administrator.", "danger")
                return redirect(url_for("login.login"))

    return render_template("index.html")


@login_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles the registration page.

    Displays the registration form and processes new user registrations.

    Returns:
        str: The HTML content rendered by the 'register.html' template.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role", "user")  # Default role is 'user'

        if register_user(username, password, role):
            return redirect(
                url_for("login.login")
            )  # Redirect to the login page after registration

    return render_template("register.html")


@login_bp.route("/logout")
def logout():
    """
    Logs out the current user and redirects to the login page.

    Returns:
        redirect: Redirects to the login page after logging out.
    """
    logout_user()
    return redirect(url_for("login.login"))


@login_bp.route("/home_user")
def home_user():
    """
    Renders the home page for regular users.

    Returns:
        str: The HTML content rendered by the 'home_user.html' template.
    """
    return render_template("home_user.html")


@login_bp.route("/admin_dashboard")
def admin_dashboard():
    """
    Renders the dashboard for administrators.

    Returns:
        str: The HTML content rendered by the 'admin_dashboard.html' template.
    """
    return render_template("admin_dashboard.html")