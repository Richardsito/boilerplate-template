
# Flask Project Boilerplate



## Step 1: Understanding the Boilerplate Structure
Every Flask project follows a structured approach to ensure scalability and readability. Here's the general structure you'll work with:
- `app.py`: The backend logic that connects routes, handles requests, and interacts with the database.
- `templates/`: Folder containing all HTML files for the web pages.
- `static/`: Folder for static assets like CSS, images, and JavaScript files.
- `app.db`: Stores all data relevant to your project.

### Key Concept
This structure ensures that your project is modular, making it easier to manage and extend for different scenarios. For example:
- In a surfboard customization tool, the focus is on user input and saving design data.
- In a booking system, the focus shifts to form validation, data storage, and user interaction.

## Step 2: Setting Up Your Boilerplate
1. **Create a New Project Folder:**
    - Open your file explorer.
    - Create a folder named `FlaskProject`.
    - Open this folder in Visual Studio Code.

2. **Create Required Files and Folders:**
    - Inside the `FlaskProject` folder, create:
        - `app.py` (backend logic).
        - `static/` (folder for stylesheets and assets).
        - `templates/` (folder for HTML pages).
        - `app.db` (SQLite database, automatically created).

3. **Install Flask:**
    - Open the terminal in Visual Studio Code.
    - Run the command:
      ```bash
      pip install flask
      ```

## Step 3: Adapting the Boilerplate
This boilerplate is flexible and can be adapted to different scenarios. Below are some examples:

### Scenario: Interactive Surfboard Customization Tool
- **Routes:** Add a route for uploading designs and viewing saved customizations.
- **Database:** Store user-generated surfboard specifications.
- **Frontend:** Create a drag-and-drop interface for customization.

### Scenario: Workshop Booking System
- **Routes:** Include routes for booking forms and viewing availability.
- **Database:** Manage data for workshops, bookings, and users.
- **Frontend:** Add date selectors and filtering options.

### Scenario: User Feedback Forum
- **Routes:** Create routes for submitting and displaying feedback.
- **Database:** Store user reviews and ratings.
- **Frontend:** Display feedback dynamically without refreshing the page.

## Step 4: Step-by-Step Code Implementation

### 1. Backend (`app.py`):
The boilerplate provides basic routes and database handling. Copy the following code into `app.py`:
```python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def connect_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('app.db')
    return conn

# Routes
@app.route('/')
def home():
    # Render the homepage
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Get data from the form
        data = request.form['input_data']
        # Connect to the database
        conn = connect_db()
        cursor = conn.cursor()
        # Insert the data into the database
        cursor.execute('INSERT INTO example_table (data) VALUES (?)', (data,))
        conn.commit()
        conn.close()
        # Redirect to the homepage after form submission
        return redirect(url_for('home'))
    # Render the form page
    return render_template('form.html')

@app.route('/data')
def data():
    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()
    # Retrieve all rows from the example_table
    cursor.execute('SELECT * FROM example_table')
    rows = cursor.fetchall()
    conn.close()
    # Render the data page with the retrieved rows
    return render_template('data.html', rows=rows)

if __name__ == '__main__':
    # Create the database table if it doesn't exist
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS example_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    # Run the Flask app in debug mode
    app.run(debug=True)
```

### Explanation:
- This boilerplate handles data input (`/form`), storage, and display (`/data`).
- Adapt the routes as needed for each scenario.

### 2. HTML Files (Frontend):
Place the following files in the `templates/` folder.

#### `index.html`: The homepage
```html
<!DOCTYPE html>
<html lang="en">
<head>
   
