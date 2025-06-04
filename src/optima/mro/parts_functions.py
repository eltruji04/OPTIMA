def create_part(part_name, part_number, aircraft_id):
    """
    Registers a new part in the database linked to a specific aircraft.

    This function inserts a new record into the `parts` table with the provided details.
    It ensures that the part is associated with a specific aircraft using the `aircraft_id`.

    Args:
        part_name (str): The name of the part.
        part_number (str): The unique identifier for the part.
        aircraft_id (int): The ID of the aircraft to which the part belongs.

    Returns:
        bool: True if the part is successfully registered, False otherwise.

    Example:
        success = create_part("Engine Filter", "EF12345", 1)
    """
    query = """
        INSERT INTO parts (part_name, part_number, aircraft_id)
        VALUES (?, ?, ?)
    """
    try:
        db_manager.execute_query(query, (part_name, part_number, aircraft_id), commit=True)
        return True
    except Exception as e:
        print(f"Error registering part: {e}")
        return False


def get_parts_by_aircraft_id(aircraft_id):
    """
    Retrieves all parts linked to a specific aircraft.

    This function queries the `parts` table to fetch all parts associated with the given `aircraft_id`.
    The results are returned as a list of dictionaries for easy consumption.

    Args:
        aircraft_id (int): The ID of the aircraft whose parts are to be retrieved.

    Returns:
        list: A list of dictionaries containing part details. Each dictionary includes:
              - id (int): The unique ID of the part.
              - part_name (str): The name of the part.
              - part_number (str): The unique identifier for the part.

    Example:
        parts = get_parts_by_aircraft_id(1)
    """
    query = """
        SELECT id, part_name, part_number FROM parts WHERE aircraft_id = ?
    """
    results = db_manager.execute_query(query, (aircraft_id,), fetch_all=True)
    return [
        {
            "id": row[0],
            "part_name": row[1],
            "part_number": row[2],
        }
        for row in results
    ]


def delete_part_by_id(part_id):
    """
    Deletes a specific part by its ID.

    This function removes a part from the `parts` table based on the provided `part_id`.
    It ensures that the deletion operation is committed to the database.

    Args:
        part_id (int): The unique ID of the part to be deleted.

    Returns:
        bool: True if the part is successfully deleted, False otherwise.

    Example:
        success = delete_part_by_id(1)
    """
    query = "DELETE FROM parts WHERE id = ?"
    try:
        db_manager.execute_query(query, (part_id,), commit=True)
        return True
    except Exception as e:
        print(f"Error deleting part: {e}")
        return False