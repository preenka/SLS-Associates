import sqlite3

conn = sqlite3.connect('sls_database.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM cases")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='cases'")

conn.commit()
conn.close()

print("All data from 'cases' table has been deleted.")
