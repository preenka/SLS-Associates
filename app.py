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

@app.route('/login', methods=['GET', 'POST'])
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

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please login first.", "error")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cases WHERE advocate_username = ?', (session['username'],))
    cases = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', username=session['username'], cases=cases)

@app.route('/logout')
def logout():
    session.clear()  # Clears everything including flash data
    flash("You have been logged out.", "info")
    return redirect('/login')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        client_name = request.form['client_name']
        title = request.form['title']
        status = request.form['status']
        next_hearing = request.form['next_hearing']
        advocate_username = session['username']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get the next case_number for this advocate
        cursor.execute('SELECT MAX(case_number) FROM cases WHERE advocate_username = ?', (advocate_username,))
        max_case_number = cursor.fetchone()[0]

        # Check if max_case_number is None or an empty string
        next_case_number = 1 if not max_case_number or max_case_number == '' else int(max_case_number) + 1

        # Insert the case with the calculated case_number
        cursor.execute(''' 
            INSERT INTO cases (advocate_username, client_name, title, status, next_hearing, case_number)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (advocate_username, client_name, title, status, next_hearing, next_case_number))

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('add.html')

@app.route('/delete_case/<int:case_id>', methods=['POST'])
def delete_case(case_id):
    if 'username' not in session:
        flash("Please login first.", "error")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Ensure the logged-in user owns this case before deleting
    cursor.execute('''
        DELETE FROM cases
        WHERE id = ? AND advocate_username = ?
    ''', (case_id, session['username']))

    conn.commit()
    conn.close()
    flash("Case deleted successfully!", "info")
    return redirect('/dashboard')

@app.route('/edit/<int:case_id>', methods=['GET', 'POST'])
def edit(case_id):
    if 'username' not in session:
        flash("Please login first.", "error")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        client_name = request.form['client_name']
        title = request.form['title']
        status = request.form['status']
        next_hearing = request.form['next_hearing']

        cursor.execute('''
            UPDATE cases
            SET client_name = ?, title = ?, status = ?, next_hearing = ?
            WHERE id = ? AND advocate_username = ?
        ''', (client_name, title, status, next_hearing, case_id, session['username']))
        conn.commit()
        conn.close()
        flash("Case updated successfully!", "success")
        return redirect('/dashboard')

    # GET: Show form with existing case data
    cursor.execute('SELECT * FROM cases WHERE id = ? AND advocate_username = ?', (case_id, session['username']))
    case = cursor.fetchone()
    conn.close()

    if not case:
        flash("Case not found.", "error")
        return redirect('/dashboard')

    return render_template('edit.html', case=case)



if __name__ == '__main__':
    app.run(debug=True)
