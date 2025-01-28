#!/usr/bin/env python3
"""Manage the active parts database."""

import logging
import sqlite3
from datetime import datetime, timedelta

LOGGER = logging.getLogger(__name__)
ACTIVE_PARTS_DB = "active_parts.db"


# Database initialization
def init_db():
    """
    Initializes the database by creating the 'items' table if it does not exist.

    This table stores information about parts, including the part number,
    item name, chapter, reminder date, and whether the notification has been shown.

    If the database does not exist, it will be created automatically.
    """
    with sqlite3.connect(ACTIVE_PARTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_number TEXT NOT NULL,
                item_name TEXT NOT NULL,
                chapter INTEGER NOT NULL,
                reminder_date TEXT,
                notification_shown INTEGER DEFAULT 0
            )
        """
        )
    LOGGER.info("Database initalized: %s", ACTIVE_PARTS_DB)


# Function to get upcoming notifications
def get_upcoming_notifications():
    """
    Retrieves notifications for parts that have an upcoming reminder date.

    Notifications are generated if the reminder date is tomorrow or today.
    Parts that have already shown a notification are filtered out.

    Returns:
        list: A list of dictionaries with the item name and notification message.
    """
    notifications = []
    today = datetime.now().date()

    with sqlite3.connect(ACTIVE_PARTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, item_name, reminder_date 
            FROM items 
            WHERE reminder_date IS NOT NULL AND notification_shown = 0
        """
        )
        items = cursor.fetchall()

        for item_id, item_name, reminder_date in items:
            if reminder_date:
                reminder_date = datetime.strptime(reminder_date, "%Y-%m-%d").date()
                if today == reminder_date - timedelta(days=1):
                    notifications.append(
                        {
                            "item_name": item_name,
                            "message": f"Tomorrow is the reminder date for '{item_name}'.",
                        }
                    )
                elif today == reminder_date:
                    notifications.append(
                        {
                            "item_name": item_name,
                            "message": f"Today is the reminder date for '{item_name}'.",
                        }
                    )

    return notifications


# Function to create a new part
def create_part(part_number, item_name, chapter, reminder_date):
    """
    Creates a new part in the database with the provided information.

    Args:
        part_number (str): The part number.
        item_name (str): The item name.
        chapter (int): The chapter number.
        reminder_date (str): The reminder date (in 'YYYY-MM-DD' format).
    """
    with sqlite3.connect("active_parts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO items (part_number, item_name, chapter, reminder_date) 
            VALUES (?, ?, ?, ?)
        """,
            (part_number, item_name, chapter, reminder_date),
        )
        conn.commit()


# Function to get all parts or a specific part
def get_parts(item_id=None):
    """
    Retrieves parts from the database. If a part ID is provided, only that part is returned.

    Args:
        item_id (int, optional): The ID of the specific part to retrieve. If not provided, all parts are returned.

    Returns:
        list: A list of parts (dictionaries) if no ID is provided, or a single dictionary if an ID is provided.
    """
    with sqlite3.connect(ACTIVE_PARTS_DB) as conn:
        cursor = conn.cursor()
        if item_id:
            cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
            item = cursor.fetchone()
            return item
        else:
            cursor.execute("SELECT * FROM items")
            items = cursor.fetchall()
            return items


# Function to update an existing part
def update_part(item_id, part_number, item_name, chapter, reminder_date):
    """
    Updates the information of an existing part in the database.

    Args:
        item_id (int): The ID of the part to update.
        part_number (str): The new part number.
        item_name (str): The new item name.
        chapter (int): The new chapter number.
        reminder_date (str): The new reminder date (in 'YYYY-MM-DD' format).
    """
    with sqlite3.connect(ACTIVE_PARTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE items 
            SET part_number = ?, item_name = ?, chapter = ?, reminder_date = ?, notification_shown = 0 
            WHERE id = ?
        """,
            (part_number, item_name, chapter, reminder_date, item_id),
        )
        conn.commit()


# Function to delete an existing part
def delete_part(item_id):
    """
    Deletes a part from the database based on its ID.

    Args:
        item_id (int): The ID of the part to delete.
    """
    with sqlite3.connect(ACTIVE_PARTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
