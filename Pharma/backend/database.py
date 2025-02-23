import sqlite3
from config import DB_FILE

def get_db_connection():
    """Connects to SQLite database and returns the connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates the tablets table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tablets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            batch_no TEXT UNIQUE NOT NULL,
            manufacturing_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ Database initialized successfully!")
