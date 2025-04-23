import pandas as pd
import json
import math

# Load CSV files
csv1 = pd.read_csv('data.csv')
csv2 = pd.read_csv('images.csv')

# Group image data by 'id' and hist-today flag
grouped_images = csv2.groupby(['id', 'hist-today'])

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

# Get images per ID and hist/today
def get_images(id_val, hist_flag):
    if (id_val, hist_flag) not in grouped_images.groups:
        return []
    images = grouped_images.get_group((id_val, hist_flag))
    return [
        {
            "image_url": wrap_nan(row["img_url"]),
            "image_credits": wrap_nan(row["img_credits"])
        } for _, row in images.iterrows()
    ]

# Build final JSON structure
metadata = []
for _, row in csv1.iterrows():
    id_val = wrap_nan(row['id'])
    metadata.append({
        "id": id_val,
        "artist": wrap_nan(row['artist']),
        "title": wrap_nan(row['title']),
        "year": wrap_nan(row['year']),
        "expo": wrap_nan(row['expo']),
        "place_today": wrap_nan(row['place_today']),
        "lat_today": safe_float(row['lat_today']),
        "lon_today": safe_float(row['lon_today']),
        "images_today": get_images(id_val, 'today'),
        "place_hist": wrap_nan(row['place_hist']),
        "lat_hist": safe_float(row['lat_hist']),
        "lon_hist": safe_float(row['lon_hist']),
        "images_hist": get_images(id_val, 'hist')
    })

# Final JSON
result = {"metadata": metadata}

# Save to file
with open('metadata.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print("✅ JSON written: metadata.json")
