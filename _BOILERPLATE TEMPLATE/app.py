from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def connect_db():
    conn = sqlite3.connect('app.db')
    return conn

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        data = request.form['input_data']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO example_table (data) VALUES (?)', (data,))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('form.html')

@app.route('/data')
def data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM example_table')
    rows = cursor.fetchall()
    conn.close()
    return render_template('data.html', rows=rows)

if __name__ == '__main__':
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS example_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    app.run(debug=True)
