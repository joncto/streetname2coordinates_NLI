# Street Name to Coordinates

This repository contains a Python script that geoparses street names into geo-coordinates. The script takes an Excel file as input, uses GeoNorge's Swagger API to retrieve the geo-coordinates for each street address, and adds the coordinates to the street address. The script then generates a new Excel file as output.

## Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- Python 3.x
- Pandas library
- Requests library

## Usage

1. Place your input Excel file in the same directory as the script.
2. Ensure that your input Excel file contains only one column (column A) with one address per row. Avoid having a column name in cell A1.
3. Run the script using the following command:

   ```shell
   python geoparse.py
