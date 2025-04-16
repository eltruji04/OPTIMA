#!/usr/bin/env python3
"""Blueprint for handling authentication-related routes."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps

# Import authentication functions
from .auth_functions import login_user, register_user, logout_user


# Create a Blueprint for authentication routes
login_bp = Blueprint(
    "login",
    __name__,
    template_folder="templates",  # Templates folder
    static_folder="static",       # Static files folder
)

# Helper function to check if the user is authenticated
def is_authenticated():
    """
    Verifies if the user is logged in.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    return "user_id" in session


# Decorator to protect routes that require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
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


# Hook to verify role-based access before processing requests
@login_bp.before_request
def check_role_access():
    public_routes = ["login.login", "login.register", "static"]
    if request.endpoint in public_routes:
        return

    if not is_authenticated():
        flash("You must log in to access this page.", "danger")
        return redirect(url_for("login.login"))

    if "admin" in request.path and session.get("role") != "admin":
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("login.home_user"))

    if "user" in request.path and session.get("role") != "user":
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("login.login"))


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
            session.permanent = True

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
@login_required
@role_required("admin")  # Solo los administradores pueden registrar usuarios
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

        # Intenta registrar al usuario
        if register_user(username, password, role):
            flash("User registered successfully.", "success")
            return redirect(url_for("login.login"))  # Redirige al inicio de sesión

        flash("An error occurred while registering the user.", "danger")

    return render_template("register.html")


@login_bp.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Logs out the current user and redirects to the login page.

    Returns:
        redirect: Redirects to the login page after logging out.
    """
    if request.method == "POST":
        session.clear()  # Limpiar la sesión
        flash("You have been logged out successfully.", "info")
        return redirect(url_for("login.login"))

    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login.login"))


# Route: Home Page for Regular Users
@login_bp.route("/home_user")
@login_required
@role_required("user")
def home_user():
    """
    Renders the home page for regular users.

    Returns:
        str: The HTML content rendered by the 'home_user.html' template.
    """
    return render_template("home_user.html")

# Route: Dashboard for Administrators
@login_bp.route("/home_admin")
@login_required
@role_required("admin")
def admin_dashboard():
    """
    Renders the dashboard for administrators.

    Returns:
        str: The HTML content rendered by the 'admin_dashboard.html' template.
    """
    return render_template("admin_home.html")