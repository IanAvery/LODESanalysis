# LODESanalysis

Python script to analyze and organize federal LODES worker origin-destination data.
Aggregates Census Block level data to particular Census Blockgroups or Census Tracts of interest.
See accompanying PDF for column metadata.

Works with Python 2 or 3.

Inputs:
  1. Raw LODES 7.0 Origin-Destination data: https://lehd.ces.census.gov/data/lodes/LODES7/
  2. List of Census Blockgroup GEOIDs or Census Tract GEOIDs of interest.

Outputs:
  This code outputs two CSVs:
  1. The areas of interest are the workplace location
  2. The areas of interest are the employee's home location

Tips for post processing:
  - Using ArcGIS create a web of employee movements:
    1. Obtain Census TIGER shapefiles of Blockgroups or Tracts
    2. Generate x and y centroids for TIGER shapefiles.
    3. Join GEOIDs to CSV results to obtain start and end x and y coordinates.
    4. Use XY to Line tool to generate lines
    5. Modify line symbology by column of interest (total workers, total workers in industrial X, etc.) 
    
    Reference: https://www.youtube.com/watch?v=0nX1_tiLgM8&feature=youtu.be
