import sqlite3
from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# Define database file
DATABASE = 'rolsa_technologies.db'

def get_db():
    """
    Connect to the SQLite database and return the connection.
    Uses the same database connection throughout the app.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Rows will be returned as dictionaries
    return conn

# Route: index (Display booking form and available slots)
@app.route('/')
def index():
    """
    Render the index page with booking form and available slots.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, day, time FROM slots WHERE booked = 0")
    slots = cursor.fetchall()
    conn.close()
    return render_template('index.html', slots=slots)

# Route: Book a slot
@app.route('/book', methods=['POST'])
def book_slot():
    """
    Book a slot and save the booking details to the database.
    """
    name = request.form.get('name')
    email = request.form.get('email')
    workshop_type = request.form.get('workshopType')
    slot_id = request.form.get('slot_id')

    if name and email and workshop_type and slot_id:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (name, email, workshop_type, slot_id) VALUES (?, ?, ?, ?)", (name, email, workshop_type, slot_id))
        cursor.execute("UPDATE slots SET booked = 1 WHERE id = ?", (slot_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

# Route: Delete a booking
@app.route('/delete_booking/<int:booking_id>')
def delete_booking(booking_id):
    """
    Delete a booking from the database.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    cursor.execute("UPDATE slots SET booked = 0 WHERE id = (SELECT slot_id FROM bookings WHERE id = ?)", (booking_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create the database and tables if they do not exist
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,
                time TEXT NOT NULL,
                booked INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                workshop_type TEXT NOT NULL,
                slot_id INTEGER NOT NULL,
                FOREIGN KEY (slot_id) REFERENCES slots (id)
            )
        """)
        conn.commit()
    # Start Flask app
    app.run(debug=True)