# LODESanalysis

Python 3 script using Pandas to analyze and organize federal LODES worker origin-destination data.
Aggregates Census Block level data to particular Census Blockgroups or Census Tracts of interest.
See accompanying PDF for column metadata.

Inputs:
  1. Raw LODES 7.0 Origin-Destination data: https://lehd.ces.census.gov/data/lodes/LODES7/
  2. List of Census Blockgroup GEOIDs or Census Tract GEOIDs of interest.

Outputs:
  This code outputs two CSVs with home GEOID, work GEOID, and quantities of workers moving:
  1. _home_: 
      - homeTractGEOID shows your GEOIDs of interest
      - workTractGEOID shows where employees in your GEOIDs go to work
  2. _work_: 
      - homeTractGEOID shows where employees in your GEOIDs are coming from
      - workTractGEOID shows your GEOIDs of interest
      
Tips for post processing:
  - Using ArcGIS create a web of employee movements:
    1. Obtain Census TIGER shapefiles of Blockgroups or Tracts
    2. Export _home_ or _work_ csv to .dbf
    3. Ensure that leading zeros are added to GEOID fields in .dbf via str(int(column)).zfill(x) x=11 for tracts, 12 for blockgroups
    5. Join _home_ or _work_ .dbf to Census Shapefiles via GEOID.
    6. Modify symbology by column of interest (total workers, total workers in industrial X, etc.) 
    
    Reference: https://www.youtube.com/watch?v=0nX1_tiLgM8&feature=youtu.be
