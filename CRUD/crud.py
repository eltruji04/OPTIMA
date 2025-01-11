from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Create the Blueprint for the CRUD functionality
crud_app = Blueprint('crud', __name__, template_folder='templates')

# Function to initialize the database
def init_db():
    """
    Initializes the database by creating the 'items' table if it doesn't exist.
    
    The table contains the following columns:
    - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
    - part_number (TEXT, NOT NULL)
    - item_name (TEXT, NOT NULL)
    - chapter (INTEGER, NOT NULL)
    
    This function is typically called once during the application's startup.
    """
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_number TEXT NOT NULL,
                item_name TEXT NOT NULL,
                chapter INTEGER NOT NULL
            )
        ''')
    print("Database initialized")

# Route to display the list of parts
@crud_app.route('/')
def parts_list():
    """
    Displays a list of all parts stored in the database.
    
    Retrieves all records from the 'items' table and renders them on the 'parts_list.html' page.
    
    Returns:
        A rendered HTML template displaying all items in the database.
    """
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()  # Fetch all records from the 'items' table
    return render_template('parts_list.html', items=items)

# Route to create a new record
@crud_app.route('/create', methods=['GET', 'POST'])
def create():
    """
    Handles the creation of a new part record in the database.
    
    If the request method is GET, it renders the 'create.html' form.
    If the request method is POST, it processes the form data, inserts a new record into the 'items' table,
    and redirects to the parts list page.
    
    Returns:
        A rendered HTML template for creating a new item if the request method is GET.
        A redirection to the parts list page if the request method is POST.
    """
    if request.method == 'POST':
        # Extract form data
        part_number = request.form['part_number']
        item_name = request.form['item_name']
        chapter = int(request.form['chapter'])

        # Insert the new item into the database
        with sqlite3.connect('active_parts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO items (part_number, item_name, chapter) VALUES (?, ?, ?)', 
                           (part_number, item_name, chapter))
            conn.commit()  # Commit the transaction
        return redirect(url_for('crud.parts_list'))  # Redirect to the parts list page
    
    return render_template('create.html')  # Render the 'create.html' form

# Route to update an existing record
@crud_app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    """
    Handles the update of an existing part record.
    
    If the request method is GET, it retrieves the part record by its ID and renders the update form.
    If the request method is POST, it processes the form data, updates the record in the database, 
    and redirects to the parts list page.
    
    Args:
        item_id (int): The ID of the item to be updated.
    
    Returns:
        A rendered HTML template for updating an item if the request method is GET.
        A redirection to the parts list page if the request method is POST.
    """
    if request.method == 'POST':
        # Extract form data
        part_number = request.form['part_number']
        item_name = request.form['item_name']
        chapter = int(request.form['chapter'])

        # Update the existing item in the database
        with sqlite3.connect('active_parts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE items SET part_number = ?, item_name = ?, chapter = ? WHERE id = ?', 
                           (part_number, item_name, chapter, item_id))
            conn.commit()  # Commit the transaction
        return redirect(url_for('crud.parts_list'))  # Redirect to the parts list page

    # Retrieve the item to be updated and render the update form
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = cursor.fetchone()  # Fetch the record with the given item_id
    return render_template('update.html', item=item)  # Render the update form with the item data

# Route to delete a record
@crud_app.route('/delete/<int:item_id>', methods=['GET', 'POST'])
def delete(item_id):
    """
    Handles the deletion of a part record from the database.
    
    Deletes the part record from the 'items' table based on the provided item ID and
    redirects to the parts list page.
    
    Args:
        item_id (int): The ID of the item to be deleted.
    
    Returns:
        A redirection to the parts list page after the item is deleted.
    """
    with sqlite3.connect('active_parts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()  # Commit the transaction
    return redirect(url_for('crud.parts_list'))  # Redirect to the parts list page
