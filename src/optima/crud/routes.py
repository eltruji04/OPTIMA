#!/usr/bin/env python3
"""Handles database paths"""

import sqlite3

from flask import Blueprint, render_template, request, redirect, url_for

from .database import (
    init_db,
    get_upcoming_notifications,
    create_part,
    get_parts,
    update_part,
)

# Create a Blueprint for CRUD functionality
crud_app = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/crud",
)

# Initialize the database (if it doesn't exist)
init_db()


# Route: Display list of parts
@crud_app.route("/")
def parts_list():
    """
    Displays all parts stored in the database along with
    notifications for upcoming reminders.

    Returns:
        render_template: Renders the 'parts_list.html' template
                          with a list of parts and upcoming notifications.
    """
    items = get_parts()
    notifications = get_upcoming_notifications()
    return render_template("parts_list.html", items=items, notifications=notifications)


# Route: Create a new part
@crud_app.route("/create", methods=["GET", "POST"])
def create():
    """
    Creates a new part in the database. If the method is GET,
    it renders the form to create a part. If the method is POST,
    it processes the form data and stores the new part.

    Returns:
        render_template or redirect: Renders the creation form or redirects to parts list after successful creation.
    """
    if request.method == "POST":
        part_number = request.form["part_number"]
        item_name = request.form["item_name"]
        chapter = int(request.form["chapter"])
        reminder_date = request.form["reminder_date"]

        # Create the part in the database
        create_part(part_number, item_name, chapter, reminder_date)
        return redirect(url_for("crud.parts_list"))

    return render_template("create.html")


# Route: Update an existing part
@crud_app.route("/update/<int:item_id>", methods=["GET", "POST"])
def update(item_id):
    """
    Updates an existing part in the database. If the method is GET,
    it fetches the part details and renders the update form. If the method
    is POST, it processes the form data and updates the part.

    Args:
        item_id (int): The ID of the part to be updated.

    Returns:
        render_template or redirect: Renders the update form or redirects to parts list after successful update.
    """
    if request.method == "POST":
        part_number = request.form["part_number"]
        item_name = request.form["item_name"]
        chapter = int(request.form["chapter"])
        reminder_date = request.form["reminder_date"]

        # Update the part in the database
        update_part(item_id, part_number, item_name, chapter, reminder_date)
        return redirect(url_for("crud.parts_list"))

    # Fetch the part details
    item = get_parts(item_id)
    if not item:
        return f"Item with ID {item_id} not found", 404

    return render_template("update.html", item=item)


# Route: Delete a part
@crud_app.route("/delete/<int:item_id>", methods=["GET", "POST"])
def delete(item_id):
    """
    Deletes a part from the database based on its ID.

    Args:
        item_id (int): The ID of the part to be deleted.

    Returns:
        redirect: Redirects to the parts list page after deletion.
    """
    with sqlite3.connect("active_parts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()

    return redirect(url_for("crud.parts_list"))
