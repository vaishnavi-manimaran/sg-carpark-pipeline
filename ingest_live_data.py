import requests
import sqlite3
from datetime import datetime

API_URL = "https://api.data.gov.sg/v1/transport/carpark-availability"
DB_NAME = "carparks.db"

def fetch_live_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    return data["items"][0]

def insert_live_data(conn, snapshot):
    cursor = conn.cursor()
    fetched_at = datetime.now().isoformat()
    rows_inserted = 0

    for entry in snapshot["carpark_data"]:
        carpark_number = entry["carpark_number"]
        update_datetime = entry["update_datetime"]

        for info in entry["carpark_info"]:
            # Some carparks have multiple lot types (C, Y, H) - we store each separately
            lots_available = info["lots_available"]
            total_lots = info["total_lots"]

            cursor.execute("""
                INSERT INTO carpark_availability
                (carpark_number, lots_available, total_lots, update_datetime, fetched_at)
                VALUES (?, ?, ?, ?, ?)
            """, (carpark_number, lots_available, total_lots, update_datetime, fetched_at))
            rows_inserted += 1

    conn.commit()
    return rows_inserted

if __name__ == "__main__":
    snapshot = fetch_live_data()
    conn = sqlite3.connect(DB_NAME)
    rows = insert_live_data(conn, snapshot)
    print(f"Inserted {rows} rows at {datetime.now().isoformat()}")
    print(f"Snapshot timestamp from API: {snapshot['timestamp']}")
    conn.close()