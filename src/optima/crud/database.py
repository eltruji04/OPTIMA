#!/usr/bin/env python3
"""
Active Parts Database Manager.

This script provides functions to manage an SQLite database that stores information about
active parts, including their part number, name, chapter, and reminder dates.

Features:
- Create and initialize the database.
- Add, retrieve, update, and delete parts.
- Manage reminder notifications for scheduled maintenance.
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager

# Configure logging
LOGGER = logging.getLogger(__name__)

# Database file name
ACTIVE_PARTS_DB = "parts.db"


class DatabaseManager:
    """
    A class to manage SQLite database connections and queries.

    This class provides methods to execute queries with optional parameters for
    committing changes and fetching results.
    """

    def __init__(self, db_path: str):
        """
        Initialize the database manager with the given database file path.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        """
        Context manager for handling database connections.

        Opens a connection to the SQLite database and ensures it is closed properly.

        Yields:
            sqlite3.Connection: The database connection object.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(
        self,
        query: str,
        params: tuple = (),
        commit: bool = False,
        fetch_one: bool = False,
        fetch_all: bool = False,
    ):
        """
        Execute an SQL query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters for the query. Defaults to ().
            commit (bool, optional): If True, commits the transaction. Defaults to False.
            fetch_one (bool, optional): If True, fetches a single result. Defaults to False.
            fetch_all (bool, optional): If True, fetches all results. Defaults to False.

        Returns:
            tuple or list: The fetched result(s) if `fetch_one` or `fetch_all` is set.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()


# Initialize the database manager
db_manager = DatabaseManager(ACTIVE_PARTS_DB)


def init_db():
    """
    Initialize the database.

    Creates the 'items' table if it does not exist.
    """
    query = """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_number TEXT NOT NULL,
            item_name TEXT NOT NULL,
            chapter INTEGER NOT NULL,
            reminder_date TEXT,
            notification_shown INTEGER DEFAULT 0
        )
    """
    db_manager.execute_query(query, commit=True)
    LOGGER.info("Database initialized: %s", ACTIVE_PARTS_DB)


def get_upcoming_notifications():
    """
    Retrieve notifications for parts with an upcoming reminder date.

    Checks if a part's reminder date is today or tomorrow and adds a notification.

    Returns:
        list: A list of notifications, each represented as a dictionary with
              'item_name' and 'message' keys.
    """
    notifications = []
    today = datetime.now().date()

    query = """
        SELECT id, item_name, reminder_date 
        FROM items 
        WHERE reminder_date IS NOT NULL AND notification_shown = 0
    """
    items = db_manager.execute_query(query, fetch_all=True)

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


def create_part(part_number: str, item_name: str, chapter: int, reminder_date: str):
    """
    Create a new part in the database.

    Args:
        part_number (str): The part number.
        item_name (str): The name of the item.
        chapter (int): The maintenance chapter number.
        reminder_date (str): The reminder date in YYYY-MM-DD format.
    """
    query = """
        INSERT INTO items (part_number, item_name, chapter, reminder_date) 
        VALUES (?, ?, ?, ?)
    """
    db_manager.execute_query(
        query, (part_number, item_name, chapter, reminder_date), commit=True
    )


def get_parts(item_id: int = None):
    """
    Retrieve parts from the database.

    If an item ID is provided, retrieves only the corresponding part; otherwise,
    retrieves all parts.

    Args:
        item_id (int, optional): The ID of the part to retrieve. Defaults to None.

    Returns:
        tuple or list: The part(s) retrieved from the database.
    """
    if item_id:
        query = "SELECT * FROM items WHERE id = ?"
        return db_manager.execute_query(query, (item_id,), fetch_one=True)
    else:
        query = "SELECT * FROM items"
        return db_manager.execute_query(query, fetch_all=True)


def update_part(
    item_id: int, part_number: str, item_name: str, chapter: int, reminder_date: str
):
    """
    Update an existing part in the database.

    Args:
        item_id (int): The ID of the part to update.
        part_number (str): The updated part number.
        item_name (str): The updated item name.
        chapter (int): The updated maintenance chapter number.
        reminder_date (str): The updated reminder date in YYYY-MM-DD format.
    """
    query = """
        UPDATE items 
        SET part_number = ?, item_name = ?, chapter = ?, reminder_date = ?, notification_shown = 0 
        WHERE id = ?
    """
    db_manager.execute_query(
        query, (part_number, item_name, chapter, reminder_date, item_id), commit=True
    )


def delete_part(item_id):
    query = "DELETE FROM items WHERE id = ?"
    db_manager.execute_query(query, (item_id,), commit=True)
    print(f"Deleted item with ID: {item_id}")


if __name__ == "__main__":
    init_db()
