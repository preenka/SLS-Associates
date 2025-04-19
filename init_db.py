import sqlite3

# Connect to the database (or create it if it doesn't exist)
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

# Insert predefined users (only if they don't already exist)
users = [
    ('Sainath', '1234'),
    ('sonu', '2004'),
    ('admin', '8998')
]

for user in users:
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', user)
    except sqlite3.IntegrityError:
        pass  # User already exists

# Create the cases table (without case_number for now)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        advocate_username TEXT NOT NULL,
        client_name TEXT NOT NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL,
        next_hearing TEXT
    )
''')

# Add case_number column if it doesn't exist
cursor.execute("PRAGMA table_info(cases)")
columns = [col[1] for col in cursor.fetchall()]
if 'case_number' not in columns:
    cursor.execute('ALTER TABLE cases ADD COLUMN case_number INTEGER')

    # Populate existing records with case_number per advocate
    cursor.execute('SELECT DISTINCT advocate_username FROM cases')
    advocates = cursor.fetchall()

    for advocate in advocates:
        advocate_username = advocate[0]
        cursor.execute('SELECT id FROM cases WHERE advocate_username = ? ORDER BY id', (advocate_username,))
        case_ids = [row[0] for row in cursor.fetchall()]
        for i, case_id in enumerate(case_ids, start=1):
            cursor.execute('UPDATE cases SET case_number = ? WHERE id = ?', (i, case_id))

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Database initialized successfully!")
print("✅ 'users' and 'cases' tables created.")
print("✅ 'case_number' column ensured and populated.")
