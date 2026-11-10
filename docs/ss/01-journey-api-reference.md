# Journey App API Reference
- Created By: Davis Boudreau
- Course: INFT300 Capstone
- Term: Winter 2025

## Pagination
- http://localhost:8000/api/origin/?page=2

## Filtering
### Usage
- http://localhost:8000/api/origin/?county=Halifax

**Filtering Options**:
  - **Find origins with "Lake" in their name**  
      http://localhost:8000/api/origin/?geoname=Lake

  - **Find origins in the county "Halifax"**  
      http://localhost:8000/api/origin/?county=Halifax

  - **Find origins with latitude greater than 45.0**  
      http://localhost:8000/api/origin/?nad83_lat__gt=45.0

  - **Find origins with longitude less than -63.0**  
      http://localhost:8000/api/origin/?nad83_lon__lt=-63.0

  - **Find origins with object IDs 1, 2, or 3**  
      http://localhost:8000/api/origin/?objectid__in=1,2,3

## Sorting 
### Usage
- http://localhost:8000/api/origin/?ordering=geoname

**Sorting Options**:
   - The `ordering_fields` list specifies the fields available for sorting data.
   - Available sorting fields are:
     - `'cgndb_key'`
     - `'geoname'`
     - `'county'`
     - `'nad83_lat'`
     - `'nad83_lon'`
     - `'locn_narr'`
   - Sorting can be applied in ascending or descending order for any of these fields.

## Sorting with Filtering and Pagination
- http://localhost:8000/api/origin/?county=Halifax&ordering=geoname&page=1