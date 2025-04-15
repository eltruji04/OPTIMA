#!/usr/bin/env python3
"""Authentication functions for user login, registration, and logout."""

from flask import session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Import the database manager from the CRUD module
from ..crud.database import db_manager


def login_user(username: str, password: str):
    """
    Authenticate a user by checking their credentials against the database.

    Args:
        username (str): The username provided by the user.
        password (str): The password provided by the user.

    Returns:
        dict: A dictionary containing user information if authentication is successful,
              or None if authentication fails.
    """
    query = "SELECT id, username, password, role FROM users WHERE username = ?"
    user = db_manager.execute_query(query, (username,), fetch_one=True)

    # Verify the password hash
    if user and check_password_hash(user[2], password):
        # Store user information in the session
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["role"] = user[3]
        return {"username": user[1], "role": user[3]}  # Return user details
    else:
        flash("Incorrect username or password.", "danger")
        return None


def register_user(username: str, password: str, role: str = "user"):
    """
    Register a new user in the database.

    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.
        role (str): The role of the new user (e.g., 'admin', 'user'). Defaults to 'user'.

    Returns:
        bool: True if registration is successful, False otherwise.
    """
    # Check if the username already exists
    query = "SELECT id FROM users WHERE username = ?"
    existing_user = db_manager.execute_query(query, (username,), fetch_one=True)
    if existing_user:
        flash("The username is already registered.", "danger")
        return False

    # Hash the password and insert the new user into the database
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    query = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
    db_manager.execute_query(query, (username, hashed_password, role), commit=True)
    flash("User registered successfully.", "success")
    return True


def logout_user():
    """
    Log out the current user by clearing the session.

    Returns:
        None
    """
    session.clear()
    flash("You have been logged out successfully.", "info")