import sqlite3

DB_NAME = 'parts.db'

def search_parts(finder):
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
    conn = sqlite3.connect(DB_NAME)
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
