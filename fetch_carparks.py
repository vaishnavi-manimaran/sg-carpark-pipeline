import requests
import json
from datetime import datetime

API_URL = "https://api.data.gov.sg/v1/transport/carpark-availability"

def fetch_carpark_data():
    response = requests.get(API_URL)
    response.raise_for_status()  # will throw an error if the request fails
    data = response.json()
    return data

if __name__ == "__main__":
    data = fetch_carpark_data()
    timestamp = data["items"][0]["timestamp"]
    carpark_count = len(data["items"][0]["carpark_data"])
    print(f"Fetched data at {timestamp}")
    print(f"Number of carparks returned: {carpark_count}")
    print("Sample record:")
    print(json.dumps(data["items"][0]["carpark_data"][0], indent=2))