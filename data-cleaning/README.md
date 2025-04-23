# Data Cleaning Workflow with OpenRefine

Cleaning workflow run on 2025-04-22 (also see the notes on manual changes below!):

1. The existing data (`UTF-8ESS-SPA_DH_25.7.24_finalfinal.xlsx`) was (partially) cleaned with OpenRefine (`cleaning.openrefine.tar.gz`) and stored as ``UTF-8ESS-SPA_DH_25.7.24_finalfinal-clean.csv`.
2. The cleaned data was then split into two files (`data.csv` and `images.csv`) which are inteded to be extended in future. The splitting process is documented in `extract-data.openrefine.tar.gz` and `extract-images.openrefine.tar.gz`.

# Notes on the Cleaning Process

## Resolved Issues

- renamed Lüginbühl → Luginbühl
- converted about 9 cells from degMinSec to decimal [using this converter](https://www.fcc.gov/media/radio/dms-decimal)
- Text transform on 54 cells in column An / Jahr: value.replace("/","–")
- One artwork has two coordinates `47.38890039002489 8.045602850675767 & 47.48801019633846 7.731032488007244`. The second coordinate was removed in the cleaning process. However, this decision should be revised

## Unresolved Issues

### Coordinates

- 2 artworks have identical coordinates for today
- 24 artworks have identical coordinates for hist
- While some coordinates appear to be precise, others are at random places in buildings
- Some of the artworks that did not move between hist and today sometimes have slightlydifferent coordinates, sometimes they overlap

### Inconsistencies

- Some credits contain `(c)`
- One exhibit seems to having been exhibited at `ESS-SPA 6, 1975 / ESS-SPA 7, 1980`. Is this true?

### Missing Information

- Missing lat/lon-today for `schrein_1979-today`
- `ESS-SPA 1997` has no ESS-number (1x)
- Missing place name (5x in hist)
- Missing image credits (5x in today)
  - https://www.publics-arts.ch/files/original/092f08d05b2ef517ab7a25063b0b17429cde2f3e.jpeg 1
  - https://www.publics-arts.ch/files/original/0ccd0184bf4fdf21de014ffc26d6bf1933b2772b.jpg 1
  - https://www.publics-arts.ch/files/original/6ea750a6558fb8216c030494e135d57d2f077b52.jpeg 1
  - https://www.publics-arts.ch/files/original/71c93ef404942f312c4e01929d63056cec219f9d.jpg 1
  - https://www.publics-arts.ch/files/original/c16f24724b8910fbf1b56fa370f5ff3a9694bc28.jpg 1

### Links

- 16MB large image on `https://www.publics-arts.ch/files/original/757c0d937e7978b7fa97f3a31d0e21b5b4ba4972.tif`
- Non-stable URL: `https://www.danielspoerri.org/giardino/wp-content/uploads/2019/04/artist-work_herbert-distel_76-1400x830.jpg`
- QR-image linked (5x in today / 6x in hist) `https://www.publics-arts.ch/files/original/1feddbfaf9f6f9c7746832045d2d5a99fcbf09f1.png`
