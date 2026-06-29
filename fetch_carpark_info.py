import requests
import json

DATASET_ID = "d_23f946fa557947f93a8043bbef41dd09"
BASE_URL = f"https://data.gov.sg/api/action/datastore_search?resource_id={DATASET_ID}"

def fetch_all_carpark_info():
    all_records = []
    offset = 0
    limit = 1000  # pull in batches of 1000

    while True:
        url = f"{BASE_URL}&limit={limit}&offset={offset}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        records = data["result"]["records"]
        if not records:
            break
        all_records.extend(records)
        offset += limit
        print(f"Fetched {len(all_records)} records so far...")
        if len(all_records) >= data["result"]["total"]:
            break

    return all_records

if __name__ == "__main__":
    records = fetch_all_carpark_info()
    print(f"\nTotal records fetched: {len(records)}")

    with open("carpark_info.json", "w") as f:
        json.dump(records, f, indent=2)
    print("Saved to carpark_info.json")