import sqlite3

# Connect to the database
conn = sqlite3.connect('sls_database.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Insert some predefined users
users = [
    ('Sainath', '1234'),
    ('sonu', '2004'),
    ('admin', '8998')
]

for user in users:
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', user)
    except sqlite3.IntegrityError:
        pass  # Skip if user already exists

conn.commit()
conn.close()

print("Database initialized and users added.")
