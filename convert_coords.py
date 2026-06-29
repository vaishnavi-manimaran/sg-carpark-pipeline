import json
from pyproj import Transformer

# SVY21 (EPSG:3414) -> WGS84 lat/lon (EPSG:4326)
transformer = Transformer.from_crs("EPSG:3414", "EPSG:4326", always_xy=True)

def svy21_to_latlon(x, y):
    lon, lat = transformer.transform(float(x), float(y))
    return lat, lon

def assign_region(lat, lon):
    if lat >= 1.38:
        return "North"
    elif lat <= 1.30:
        return "South"
    elif lon <= 103.75:
        return "West"
    elif lon >= 103.87:
        return "East"
    else:
        return "Central"

if __name__ == "__main__":
    with open("carpark_info.json", "r") as f:
        records = json.load(f)

    for record in records:
        lat, lon = svy21_to_latlon(record["x_coord"], record["y_coord"])
        record["latitude"] = lat
        record["longitude"] = lon
        record["region"] = assign_region(lat, lon)

    with open("carpark_info_with_location.json", "w") as f:
        json.dump(records, f, indent=2)

    print(f"Converted {len(records)} records.")
    print("Sample converted record:")
    print(json.dumps(records[0], indent=2))