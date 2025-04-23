import pandas as pd
import json
import math

# Load the CSV
csv = pd.read_csv('data.csv')

features = []


# Helper: Wrap NaN values (string or float) as "NaN"
def wrap_nan(val):
    if pd.isna(val) or (isinstance(val, float) and math.isnan(val)):
        return "NaN"
    return val

# Helper: Convert numeric values, or wrap NaN
def safe_float(val):
    try:
        f = float(val)
        return "NaN" if math.isnan(f) else f
    except:
        return "NaN"


for _, row in csv.iterrows():
    id_val = wrap_nan(row['id'])
    
    # Point feature - today
    features.append({
        "type": "Feature",
        "id": f"{id_val}-today",
        "properties": {
            "id": id_val,
            "today_hist": "today"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [safe_float(row['lon_today']), safe_float(row['lat_today'])]
        }
    })
    
    # Point feature - hist
    features.append({
        "type": "Feature",
        "id": f"{id_val}-hist",
        "properties": {
            "id": id_val,
            "today_hist": "hist"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [safe_float(row['lon_hist']), safe_float(row['lat_hist'])]
        }
    })

    # LineString connecting the two
    features.append({
        "type": "Feature",
        "id": f"{id_val}-line",
        "properties": {
            "id": id_val,
            "today_hist": "line"
        },
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [safe_float(row['lon_hist']), safe_float(row['lat_hist'])],
                [safe_float(row['lon_today']), safe_float(row['lat_today'])]
            ]
        }
    })

# Full GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Write to file
with open('features.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False, indent=4)

print("GeoJSON file created: features.geojson")
