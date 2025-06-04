from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .aircraft_functions import (
    get_all_aircraft,
    register_aircraft,
    update_aircraft,
    delete_aircraft_by_id,
    get_aircraft_by_id,
    create_part,
    get_parts_by_aircraft_id,
    delete_part_by_id,
)


# Create a Blueprint for the MRO module
mro_bp = Blueprint(
    "mro",
    __name__,
    template_folder="templates",  # Folder containing HTML templates
    static_folder="static",       # Folder containing static files (CSS, JS, etc.)
)


@mro_bp.route("/", methods=["GET"])
def index():
    """
    Main page of the MRO module.
    Redirects to the aircraft management view.

    Returns:
        redirect: Redirects to the `mro.aircraft` route.
    """
    return redirect(url_for("mro.aircraft"))


@mro_bp.route("/aircraft", methods=["GET", "POST"])
def aircraft():
    """
    Manages the aircraft view.
    - GET: Displays the form to add a new aircraft and lists all registered aircraft.
    - POST: Processes the form to register a new aircraft.

    Returns:
        str: Renders the `aircraft.html` template with the list of aircraft or redirects after registration.
    """
    if request.method == "POST":
        try:
            model = request.form.get("model")
            registration = request.form.get("registration")
            year_of_manufacture = int(request.form.get("year_of_manufacture"))
            manufacturer = request.form.get("manufacturer")
            passenger_capacity = request.form.get("passenger_capacity")

            success = register_aircraft(
                model=model,
                registration=registration,
                year_of_manufacture=year_of_manufacture,
                manufacturer=manufacturer,
                passenger_capacity=int(passenger_capacity) if passenger_capacity else None,
            )
            if success:
                flash("Aircraft registered successfully.", "success")
            else:
                flash("Error registering the aircraft.", "danger")
            return redirect(url_for("mro.aircraft"))
        except Exception as e:
            flash(f"Unexpected error: {e}", "danger")
            return redirect(url_for("mro.aircraft"))

    aircraft_list = get_all_aircraft()
    return render_template("aircraft.html", aircraft_list=aircraft_list, current_year=datetime.now().year)


@mro_bp.route("/edit/<int:aircraft_id>", methods=["GET", "POST"])
def edit_aircraft(aircraft_id):
    """
    Manages the editing of an existing aircraft.
    - GET: Displays the edit form with the current aircraft details.
    - POST: Processes the form to update the aircraft details.

    Args:
        aircraft_id (int): The ID of the aircraft to edit.

    Returns:
        str: Renders the `edit_aircraft.html` template or redirects after updating.
    """
    # Retrieve the aircraft by its ID
    aircraft = get_aircraft_by_id(aircraft_id)
    if not aircraft:
        flash("The aircraft does not exist.", "danger")
        return redirect(url_for("mro.aircraft"))

    if request.method == "POST":
        try:
            model = request.form.get("model")
            registration = request.form.get("registration")
            year_of_manufacture = int(request.form.get("year_of_manufacture"))
            manufacturer = request.form.get("manufacturer")
            passenger_capacity = request.form.get("passenger_capacity", default=None)

            # Additional validations
            current_year = datetime.now().year
            if year_of_manufacture > current_year:
                flash("The year of manufacture cannot be greater than the current year.", "danger")
                return render_template("edit_aircraft.html", aircraft=aircraft, current_year=current_year)

            # Update the aircraft
            success = update_aircraft(
                aircraft_id=aircraft_id,
                model=model,
                registration=registration,
                year_of_manufacture=year_of_manufacture,
                manufacturer=manufacturer,
                passenger_capacity=int(passenger_capacity) if passenger_capacity else None,
            )
            if success:
                flash("Aircraft updated successfully.", "success")
                return redirect(url_for("mro.aircraft"))
            else:
                flash("Error updating the aircraft. Please try again.", "danger")
                return render_template("edit_aircraft.html", aircraft=aircraft, current_year=current_year)
        except Exception as e:
            # Log unexpected errors
            print(f"Error processing the form: {e}")
            flash("An unexpected error occurred. Please try again later.", "danger")
            return render_template("edit_aircraft.html", aircraft=aircraft, current_year=datetime.now().year)

    # Render the edit form with the current aircraft details
    return render_template("edit_aircraft.html", aircraft=aircraft, current_year=datetime.now().year)


@mro_bp.route("/delete/<int:aircraft_id>", methods=["POST"])
def delete_aircraft(aircraft_id):
    """
    Deletes an existing aircraft.

    Args:
        aircraft_id (int): The ID of the aircraft to delete.

    Returns:
        redirect: Redirects to the `mro.aircraft` route after deletion.
    """
    success = delete_aircraft_by_id(aircraft_id)
    if success:
        flash("Aircraft deleted successfully.", "success")
    else:
        flash("Error deleting the aircraft.", "danger")
    return redirect(url_for("mro.aircraft"))


@mro_bp.route("/aircraft/<int:aircraft_id>/parts", methods=["GET", "POST"])
def aircraft_parts(aircraft_id):
    """
    Manages parts linked to a specific aircraft.
    - GET: Displays the parts linked to the aircraft.
    - POST: Adds a new part linked to the aircraft.

    Args:
        aircraft_id (int): The ID of the aircraft.

    Returns:
        str: Renders the `aircraft_parts.html` template or redirects after adding a part.
    """
    # Retrieve the aircraft by its ID
    aircraft = get_aircraft_by_id(aircraft_id)
    if not aircraft:
        flash("The aircraft does not exist.", "danger")
        return redirect(url_for("mro.aircraft"))

    if request.method == "POST":
        try:
            part_name = request.form["part_name"]
            part_number = request.form["part_number"]

            # Create the part linked to the aircraft
            success = create_part(part_name, part_number, aircraft_id)
            if success:
                flash("Part registered successfully.", "success")
            else:
                flash("Error registering the part.", "danger")
            return redirect(url_for("mro.aircraft_parts", aircraft_id=aircraft_id))
        except Exception as e:
            flash(f"Unexpected error: {e}", "danger")
            return redirect(url_for("mro.aircraft_parts", aircraft_id=aircraft_id))

    # Retrieve the parts linked to the aircraft
    parts = get_parts_by_aircraft_id(aircraft_id)
    return render_template("aircraft_parts.html", aircraft=aircraft, parts=parts)


@mro_bp.route("/delete-part/<int:part_id>", methods=["POST"])
def delete_part(part_id):
    """
    Deletes a specific part.

    Args:
        part_id (int): The ID of the part to delete.

    Returns:
        redirect: Redirects to the referring page after deletion.
    """
    success = delete_part_by_id(part_id)
    if success:
        flash("Part deleted successfully.", "success")
    else:
        flash("Error deleting the part.", "danger")
    return redirect(request.referrer)