
import sqlite3

def db_init():
    # Connect to the SQLite database (creates a new file if it doesn't exist)
    conn = sqlite3.connect('example.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Delete the table if it exists
    cursor.execute("DROP TABLE IF EXISTS skill")

    # Commit the changes to the database
    conn.commit()

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS skill (
                    skill TEXT PRIMARY KEY,
                    freq INTEGER NOT NULL,
                    freq_threshold INTEGER,
                    importance real DEFAULT 0)''')
    
    return conn, cursor
