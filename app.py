from flask import Flask, render_template, request, flash, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key"

def get_db_connection():
    conn = sqlite3.connect('sls_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user exists with matching username and password
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            flash("Login successful!", "success")
        else:
            flash("Invalid credentials. Try again.", "error")

        return redirect('/')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
