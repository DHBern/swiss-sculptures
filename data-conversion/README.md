# Step 1: Add new data

- Add information on the artwork to `data.csv`
- Add information on the images (url and credits) to `images.csv`
- Make sure that the data shares the same unique `id`
  - Currently, this is a string containing the name of the artwork and the ess-spa-year. Avoid special characters and whitespaces

# Step 2: Create features.geojson

Converts `data.csv` into `features.geojson`

```bash
python3 ./convert-features.py
```

# Step 3: Create metadata.json

Converts `data.csv` and `images.csv` into `metadata.json`

```bash
python3 ./convert-metadatadata.py
```

# Step 4: Move or copy features.geojson and metadata.json to the static folder
