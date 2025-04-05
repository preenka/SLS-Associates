from flask import Flask, render_template, request, flash, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key"

def get_db_connection():
    conn = sqlite3.connect('sls_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/login', methods=['GET', 'POST'])  # ✅ Allows both GET and POST
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            flash("Login successful!", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid credentials. Try again.", "error")
            return redirect('/login')

    return render_template('login.html')  # When method is GET

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please login first.", "error")
        return redirect('/login')
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
