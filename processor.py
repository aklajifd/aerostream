import sys
import sqlite3
from datetime import datetime

def setup_database():
    # Create a file named 'satellite_data.db'
    conn = sqlite3.connect('satellite_data.db')
    cursor = conn.cursor()

    # Create a table to store our telemetry
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telemetry_type TEXT,
            raw_message TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    return conn

def main():
    print("--- Python Consumer with Database Started ---")
    db_conn = setup_database()
    cursor = db_conn.cursor()

    for line in sys.stdin:
        clean_data = line.strip()

        start = clean_data.find("[") + 1
        end = clean_data.find("]")
        tele_type = clean_data[start:end] if start > 0 else "UNKNOWN"

        # Save to Database
        now = datetime.now()
        cursor.execute(
            "INSERT INTO telemetry (telemetry_type, raw_message, timestamp) VALUES (?, ?, ?)",
            (tele_type, clean_data, now)
        )
        db_conn.commit()

        print(f"Stored: {tele_type} at {now.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()