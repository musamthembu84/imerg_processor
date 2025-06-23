# IMERG Daily Precipitation Downloader

This project provides a Python utility for downloading and cropping **daily precipitation data** from the [NASA GPM IMERG Final Run Dataset (GPM_3IMERGDF)](https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDF_07/summary) for a specific country or region.

It uses NASA's authenticated API to fetch `.nc4` NetCDF4 files, extracts only the specified geographic region, and stores the output in a local folder for further use in climate studies, hydrological modeling, agriculture, or machine learning.

---

## What This Project Does

- Downloads **daily precipitation data** from NASA's GESDISC archive.
- Crops the data to a given **latitude/longitude box** (e.g. your country).
- Saves the cropped `.nc4` files to a local folder.
- Automatically skips already downloaded files.

---

## Requirements

Ensure you have Python 3.8+ installed.

Install dependencies using:

```bash
pip install -r requirements.txt

Files and Structure

├── imerg_main.py          # Entry-point script
├── imerg_processor.py     # Core download + processing logic
├── .env                   # Configuration for credentials, coordinates, etc.
├── requirements.txt       # Python dependencies
└── imerg_data/            # Output directory for downloaded .nc4 files


Environment Configuration
# NASA Earthdata Login Credentials
# These are required to authenticate your downloads from the GESDISC archive.
# Get these by registering at: https://urs.earthdata.nasa.gov
GESDISC_USERNAME=your_nasa_earthdata_username
GESDISC_TOKEN=your_nasa_earthdata_token

# Base URL for the GPM IMERG Final Daily Dataset (Version 07B)
# This URL points to the top-level directory where all daily data is stored.
BASE_URL=https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.07

# The name of your target country or region
# This will be used in the output filenames for clarity.
COUNTRY_NAME=Kenya

# Date range for downloading data (inclusive)
# Format: YYYY-MM-DD
START_DATE=2022-01-01   # Start downloading from this date
END_DATE=2022-01-10     # End on this date

# Geographical bounding box for the region you want to crop
# Coordinates are in decimal degrees

LAT_NORTH=5.0   # Northernmost latitude
LAT_SOUTH=-5.0  # Southernmost latitude
LON_EAST=42.0   # Easternmost longitude
LON_WEST=33.0   # Westernmost longitude

# Local folder where downloaded and processed files will be stored
# This folder will be created if it doesn't exist.
OUTPUT_DIR=imerg_data


