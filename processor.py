import sys
import sqlite3
import requests
from datetime import datetime

def get_real_iss_data():
    try:
        # Official "Where is the ISS At?" API
        response = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
        data = response.json()
        lat = round(data['latitude'], 4)
        lon = round(data['longitude'], 4)
        vel = round(data['velocity'], 2)
        return f"ISS LIVE -> Lat: {lat}, Lon: {lon} | Velocity: {vel} km/h"
    except Exception:
        return "ISS API Offline - Using Simulated Data"

def setup_database():
    # Create a file named 'satellite_data.db'
    conn = sqlite3.connect('satellite_data.db')
    cursor = conn.cursor()
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
    print("--- AeroStream Processor (LIVE API MODE) ---")
    db_conn = setup_database()
    cursor = db_conn.cursor()

    for line in sys.stdin:
        clean_data = line.strip()

        # Check for GPS packet
        if "[GPS]" in clean_data:
            real_info = get_real_iss_data()
            display_msg = f"[GPS] {real_info}"
        else:
            display_msg = clean_data

        # Determine type for DB
        tele_type = "GPS" if "[GPS]" in clean_data else ("POWER" if "[POWER]" in clean_data else "THERMAL")

        # Save to DB
        now = datetime.now()
        cursor.execute(
            "INSERT INTO telemetry (telemetry_type, raw_message, timestamp) VALUES (?, ?, ?)",
            (tele_type, display_msg, now)
        )
        db_conn.commit()
        print(f"Logged: {display_msg}")

if __name__ == "__main__":
    main()