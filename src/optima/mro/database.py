import sqlite3


class DBManager:
    """
    A utility class to manage SQLite database operations.

    This class provides a simple interface for executing SQL queries,
    handling transactions, and fetching results. It ensures that database
    connections are properly managed using context managers.

    Attributes:
        db_name (str): The name of the SQLite database file.
    """

    def __init__(self, db_name="parts.db"):
        """
        Initializes the DBManager with the specified database file.

        Args:
            db_name (str): The name of the SQLite database file. Defaults to "parts.db".
        """
        self.db_name = db_name

    def execute_query(
        self, query, params=None, fetch_one=False, fetch_all=False, commit=False
    ):
        """
        Executes a SQL query on the database.

        This method supports parameterized queries, fetching results, and committing transactions.
        It uses a context manager to ensure that the database connection is properly closed.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to bind to the query. Defaults to None.
            fetch_one (bool, optional): If True, fetches a single result row. Defaults to False.
            fetch_all (bool, optional): If True, fetches all result rows. Defaults to False.
            commit (bool, optional): If True, commits the transaction after execution. Defaults to False.

        Returns:
            tuple or list or None: The fetched result(s) if `fetch_one` or `fetch_all` is True,
                                   otherwise None. Returns None in case of an error.

        Example:
            # Insert a new record
            db_manager.execute_query(
                "INSERT INTO items (name, value) VALUES (?, ?)", ("Item1", 100), commit=True
            )

            # Fetch a single record
            result = db_manager.execute_query("SELECT * FROM items WHERE id = ?", (1,), fetch_one=True)
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if commit:
                    conn.commit()

                if fetch_one:
                    return cursor.fetchone()
                if fetch_all:
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None


# Global instance of DBManager
db_manager = DBManager()