from datetime import datetime
from optima.crud.database import db_manager


def register_aircraft(
    model,
    registration,
    year_of_manufacture,
    manufacturer,
    passenger_capacity=None,
    status="Active",
    total_flight_hours=0,
    cycles=0,
    owner_operator=None,
    last_inspection_date=None,
    current_location=None,
):
    """
    Registers a new aircraft in the database.

    Args:
        model (str): The aircraft's model.
        registration (str): The aircraft's registration number (unique identifier).
        year_of_manufacture (int): The year the aircraft was manufactured.
        manufacturer (str): The aircraft's manufacturer.
        passenger_capacity (int, optional): The aircraft's passenger capacity. Defaults to None.
        status (str, optional): The aircraft's operational status. Defaults to "Active".
        total_flight_hours (float, optional): Total flight hours logged. Defaults to 0.
        cycles (int, optional): Total flight cycles logged. Defaults to 0.
        owner_operator (str, optional): The aircraft's owner or operator. Defaults to None.
        last_inspection_date (datetime, optional): The date of the last inspection. Defaults to None.
        current_location (str, optional): The aircraft's current location. Defaults to None.

    Returns:
        bool: True if the aircraft is registered successfully, False otherwise.

    Example:
        register_aircraft("Boeing 747", "N12345", 2005, "Boeing", passenger_capacity=400)
    """
    # Check if the registration already exists
    query_check = "SELECT id FROM aircraft WHERE registration = ?"
    existing_aircraft = db_manager.execute_query(query_check, (registration,), fetch_one=True)
    if existing_aircraft:
        print(f"Error: Aircraft with registration '{registration}' is already registered.")
        return False

    # Insert the new aircraft
    query_insert = """
        INSERT INTO aircraft (
            model, registration, year_of_manufacture, manufacturer, 
            passenger_capacity, status, total_flight_hours, cycles, 
            owner_operator, last_inspection_date, current_location
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        model,
        registration,
        year_of_manufacture,
        manufacturer,
        passenger_capacity,
        status,
        total_flight_hours,
        cycles,
        owner_operator,
        last_inspection_date,
        current_location,
    )
    try:
        db_manager.execute_query(query_insert, params, commit=True)
        print(f"Aircraft '{model}' with registration '{registration}' registered successfully.")
        return True
    except Exception as e:
        print(f"Error registering aircraft: {e}")
        return False


def get_all_aircraft():
    """
    Retrieves all aircraft registered in the database.

    Returns:
        list: A list of dictionaries containing aircraft details. Each dictionary includes:
              - id (int): The aircraft's unique ID.
              - model (str): The aircraft's model.
              - registration (str): The aircraft's registration number.
              - year_of_manufacture (int): The year the aircraft was manufactured.
              - manufacturer (str): The aircraft's manufacturer.
              - passenger_capacity (int): The aircraft's passenger capacity.
              - status (str): The aircraft's operational status.
              - total_flight_hours (float): Total flight hours logged.
              - cycles (int): Total flight cycles logged.
              - owner_operator (str): The aircraft's owner or operator.
              - last_inspection_date (datetime): The date of the last inspection.
              - current_location (str): The aircraft's current location.

    Example:
        aircraft_list = get_all_aircraft()
    """
    query = "SELECT * FROM aircraft"
    try:
        rows = db_manager.execute_query(query, fetch_all=True)
        aircraft_list = []
        for row in rows:
            aircraft = {
                "id": row[0],
                "model": row[1],
                "registration": row[2],
                "year_of_manufacture": row[3],
                "manufacturer": row[4],
                "passenger_capacity": row[5],
                "status": row[6],
                "total_flight_hours": row[7],
                "cycles": row[8],
                "owner_operator": row[9],
                "last_inspection_date": row[10],
                "current_location": row[11],
            }
            aircraft_list.append(aircraft)
        return aircraft_list
    except Exception as e:
        print(f"Error retrieving aircraft: {e}")
        return []


def get_aircraft_by_id(aircraft_id):
    """
    Retrieves the details of an aircraft by its ID.

    Args:
        aircraft_id (int): The unique ID of the aircraft.

    Returns:
        dict or None: A dictionary containing the aircraft's details if found, or None if not found.

    Example:
        aircraft = get_aircraft_by_id(1)
    """
    query = "SELECT id, model, registration, year_of_manufacture, manufacturer, passenger_capacity FROM aircraft WHERE id = ?"
    try:
        result = db_manager.execute_query(query, (aircraft_id,), fetch_one=True)
        if result:
            return {
                "id": result[0],
                "model": result[1],
                "registration": result[2],
                "year_of_manufacture": result[3],
                "manufacturer": result[4],
                "passenger_capacity": result[5],
            }
        return None
    except Exception as e:
        print(f"Error retrieving aircraft by ID: {e}")
        return None


def delete_aircraft_by_id(aircraft_id):
    """
    Deletes an aircraft by its ID.

    Args:
        aircraft_id (int): The unique ID of the aircraft.

    Returns:
        bool: True if the aircraft is deleted successfully, False otherwise.

    Example:
        success = delete_aircraft_by_id(1)
    """
    query = "DELETE FROM aircraft WHERE id = ?"
    try:
        db_manager.execute_query(query, (aircraft_id,), commit=True)
        return True
    except Exception as e:
        print(f"Error deleting aircraft: {e}")
        return False


def update_aircraft(
    aircraft_id,
    model,
    registration,
    year_of_manufacture,
    manufacturer,
    passenger_capacity,
):
    """
    Updates the details of an existing aircraft.

    Args:
        aircraft_id (int): The unique ID of the aircraft.
        model (str): The updated aircraft model.
        registration (str): The updated registration number.
        year_of_manufacture (int): The updated year of manufacture.
        manufacturer (str): The updated manufacturer.
        passenger_capacity (int): The updated passenger capacity.

    Returns:
        bool: True if the aircraft is updated successfully, False otherwise.

    Example:
        success = update_aircraft(1, "Boeing 747-8", "N12345", 2010, "Boeing", 416)
    """
    query = """
        UPDATE aircraft
        SET model = ?, registration = ?, year_of_manufacture = ?, manufacturer = ?, passenger_capacity = ?
        WHERE id = ?
    """
    try:
        db_manager.execute_query(
            query,
            (
                model,
                registration,
                year_of_manufacture,
                manufacturer,
                passenger_capacity,
                aircraft_id,
            ),
            commit=True,
        )
        return True
    except Exception as e:
        print(f"Error updating aircraft: {e}")
        return False


def create_part(part_name, part_number, aircraft_id):
    """
    Registers a new part in the database linked to a specific aircraft.

    Args:
        part_name (str): The name of the part.
        part_number (str): The unique part number.
        aircraft_id (int): The ID of the aircraft to which the part belongs.

    Returns:
        bool: True if the part is registered successfully, False otherwise.

    Example:
        success = create_part("Engine Filter", "EF12345", 1)
    """
    # Check if the part number already exists
    query_check = "SELECT id FROM aircraft_parts WHERE part_number = ?"
    existing_part = db_manager.execute_query(query_check, (part_number,), fetch_one=True)
    if existing_part:
        print(f"Error: Part number '{part_number}' is already registered.")
        return False

    # Insert the new part
    query = """
        INSERT INTO aircraft_parts (part_name, part_number, aircraft_id, total_flight_hours)
        VALUES (?, ?, ?, 0)
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

    Args:
        aircraft_id (int): The ID of the aircraft.

    Returns:
        list: A list of dictionaries containing part details. Each dictionary includes:
              - id (int): The part's unique ID.
              - part_name (str): The name of the part.
              - part_number (str): The unique part number.
              - total_flight_hours (float): Total flight hours logged for the part.

    Example:
        parts = get_parts_by_aircraft_id(1)
    """
    query = """
        SELECT id, part_name, part_number, total_flight_hours
        FROM aircraft_parts
        WHERE aircraft_id = ?
    """
    try:
        results = db_manager.execute_query(query, (aircraft_id,), fetch_all=True)
        return [
            {
                "id": row[0],
                "part_name": row[1],
                "part_number": row[2],
                "total_flight_hours": row[3],
            }
            for row in results
        ]
    except Exception as e:
        print(f"Error retrieving parts by aircraft ID: {e}")
        return []


def delete_part_by_id(part_id):
    """
    Deletes a specific part by its ID.

    Args:
        part_id (int): The unique ID of the part.

    Returns:
        bool: True if the part is deleted successfully, False otherwise.

    Example:
        success = delete_part_by_id(1)
    """
    query = "DELETE FROM aircraft_parts WHERE id = ?"
    try:
        db_manager.execute_query(query, (part_id,), commit=True)
        return True
    except Exception as e:
        print(f"Error deleting part: {e}")
        return False