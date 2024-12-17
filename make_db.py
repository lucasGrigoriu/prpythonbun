import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')  # 'mydatabase.db' is the SQLite database file
cursor = conn.cursor()

# Create a new table called 'users'

cursor.execute('''
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER,
    beds INTEGER,
    ppn INTEGER,
    rating REAL,
    no_ratings INTEGER
)
''')

# Create a new table called 'products'

cursor.execute('''
CREATE TABLE IF NOT EXISTS accomodations (
    id INTEGER,
    room_id INTEGER,
    date_start DATE,
    date_end DATE ,
    name TEXT
)
''')

# Commit the changes to the database
conn.commit()

# Verify the tables have been created by fetching the list of tables


# Close the connection
conn.close()
