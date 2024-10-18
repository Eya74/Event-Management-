import sqlite3
import os

# Get the path to your events.db file
db_path = 'events.db'  # Update this if your database file is named differently or in a different location

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def show_table_info():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(events)")
    columns = cursor.fetchall()
    conn.close()
    
    print("Current columns in the events table:")
    for column in columns:
        print(f"- {column['name']} ({column['type']})")

def add_description_column():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE events ADD COLUMN description TEXT")
        conn.commit()
        print("\nSuccessfully added 'description' column to the events table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("\n'description' column already exists in the events table.")
        else:
            print(f"\nAn error occurred: {e}")
    finally:
        conn.close()

def main():
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found.")
        return

    print("Before update:")
    show_table_info()

    add_description_column()

    print("\nAfter update:")
    show_table_info()

if __name__ == "__main__":
    main()