import sqlite3
import json

DB_NAME = "carparks.db"

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carparks (
            car_park_no TEXT PRIMARY KEY,
            address TEXT,
            car_park_type TEXT,
            type_of_parking_system TEXT,
            free_parking TEXT,
            night_parking TEXT,
            gantry_height TEXT,
            latitude REAL,
            longitude REAL,
            region TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carpark_availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carpark_number TEXT,
            lots_available INTEGER,
            total_lots INTEGER,
            update_datetime TEXT,
            fetched_at TEXT
        )
    """)

    conn.commit()

def load_static_carparks(conn):
    with open("carpark_info_with_location.json", "r") as f:
        records = json.load(f)

    cursor = conn.cursor()
    for r in records:
        cursor.execute("""
            INSERT OR REPLACE INTO carparks
            (car_park_no, address, car_park_type, type_of_parking_system,
             free_parking, night_parking, gantry_height, latitude, longitude, region)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["car_park_no"], r["address"], r["car_park_type"],
            r["type_of_parking_system"], r["free_parking"], r["night_parking"],
            r["gantry_height"], r["latitude"], r["longitude"], r["region"]
        ))

    conn.commit()
    print(f"Loaded {len(records)} static carpark records into 'carparks' table.")

if __name__ == "__main__":
    conn = sqlite3.connect(DB_NAME)
    create_tables(conn)
    load_static_carparks(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM carparks")
    count = cursor.fetchone()[0]
    print(f"Total rows in 'carparks' table: {count}")

    cursor.execute("SELECT * FROM carparks LIMIT 1")
    print("Sample row:", cursor.fetchone())

    conn.close()