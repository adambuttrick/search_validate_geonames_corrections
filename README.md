# README for CSV Geonames Enhancer

## Overview
Search for the Geonames IDs of city corrections, as well as verify current ROR assignments.

## Requirements
- Python 3.x
- `requests` library
- `csv` module
- `thefuzz` library
- Geonames user name

## Installation
Ensure Python 3.x and pip are installed. Run:
```bash
pip install -r requirements.txt
```

## Usage
```bash
python search_validate_geonames_corrections.py -i <input_csv> -o <output_csv> -u <geonames_user>
```
- `-i` / `--input_csv`: Path to the input CSV file.
- `-o` / `--output_csv`: Path to the output CSV file.
- `-u` / `--geonames_user`: Geonames user name.

## Functionality
- Reads an input CSV file.
- Queries the ROR (Research Organization Registry) API for each row.
- Parse Geonames ID and city from ROR record
- Queries the Geonames API for city information.
- Outputs matched Geonames data to a specified CSV file.

## Input File Format
The input CSV must contain the following headers:
- `ror_id`: ROR identifier.
- `city_corrected`: Corrected city name.

## Output File Format
The output CSV will contain the following additional headers:
- `ror_geonames_id`: Geonames ID from ROR query.
- `ror_geonames_name`: Geonames city name from ROR query.
- `city_corrected_geonames_id`: Geonames ID from direct query.
- `city_corrected_geonames_name`: Geonames city name from direct query.