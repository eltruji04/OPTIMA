import sqlite3

# Nombre de la base de datos
DB_NAME = 'parts.db'


def search_parts(finder):
    """
    Searches for parts in the database that match the given query.

    Parameters:
        finder (str): The search term used to find matching parts 
                      in the database. It can be part number or item name.

    Returns:
        list: A list of tuples representing rows from the 
              Parts table that match the search term. Each tuple contains the 
              data of a matching part.
    
    Example:
        search_parts('brake') 
        Returns a list of parts where part number or item name contains 'brake'.
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
