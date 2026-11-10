
## Get Origin API Usage

This API provides access to Origin objects with pagination, filtering, and sorting capabilities.

### 1. Basic List Retrieval

- **Endpoint:** `GET /api/origin/`
- **Description:** Retrieves a paginated list of all Origin objects.
- **Examples:**

  ```bash
  curl http://localhost:8000/api/v1/stn/GetOrigin
  ```

  ```http
  http://localhost:8000/api/v1/stn/GetOrigin
  ```

### 2. Pagination

- **Parameters:**
  - `page`: Page number (integer).
  - `page_size`: Number of items per page (integer, max 100). Default is 25.

- **Examples:**
  - Get page 2:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?page=2
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?page=2
    ```

  - Get 50 items per page:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?page_size=50
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?page_size=50
    ```

  - Get page 2, 50 items per page:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?page=2&page_size=50
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?page=2&page_size=50
    ```

### 3. Filtering

- **Parameters:**
  - `geoname__icontains`: Filter by geoname (case-insensitive contains).
  - `county__icontains`: Filter by county (case-insensitive contains).
  - `nad83_lat__gt`: Filter by latitude greater than a value.
  - `nad83_lon__lt`: Filter by longitude less than a value.
  - `objectid__in`: Filter by objectid(s) within a comma-separated list.

- **Examples:**
  - Filter by geoname containing "geoname":

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?geoname__icontains=geoname
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?geoname__icontains=geoname
    ```

  - Filter by county containing "county":

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?county__icontains=county
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?county__icontains=county
    ```

  - Filter by latitude greater than 40:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?nad83_lat__gt=40
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?nad83_lat__gt=40
    ```

  - Filter by longitude less than -70:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?nad83_lon__lt=-70
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?nad83_lon__lt=-70
    ```

  - Filter by objectid 1, 2, and 3:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?objectid__in=1,2,3
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?objectid__in=1,2,3
    ```

### 4. Sorting

- **Parameter:**
  - `ordering`: Field to sort by. Prefix with "-" for descending order.
  - Supported fields: `objectid`, `geoname`, `county`, `nad83_lat`, `nad83_lon`.

- **Examples:**
  - Sort by geoname ascending:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?ordering=geoname
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?ordering=geoname
    ```

  - Sort by county descending:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?ordering=-county
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?ordering=-county
    ```

  - Sort by latitude ascending:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?ordering=nad83_lat
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?ordering=nad83_lat
    ```

### 5. Combination of Pagination, Filtering, and Sorting

- **Example:**
  - Get page 2, 20 items per page, filter by geoname containing "geoname", and sort by county descending:

    ```bash
    curl http://localhost:8000/api/v1/stn/GetOrigin?page=2&page_size=20&geoname__icontains=geoname&ordering=-county
    ```

    ```http
    http://localhost:8000/api/v1/stn/GetOrigin?page=2&page_size=20&geoname__icontains=geoname&ordering=-county
    ```

### 6. Error Handling

- **Invalid Filter/Sort Field:**
  - Returns HTTP 400 Bad Request with an error message.

- **Invalid Page/Page Size:**
  - Returns HTTP 400 Bad Request with an error message.

- **Invalid data within filter parameters:**
  - Returns HTTP 400 Bad Request with an error message.

- **Internal Server Error:**
  - Returns HTTP 500 Internal Server Error with an error message and an error ID for support.

### 7. Serialized Data

- The API returns JSON data representing Origin objects, including fields like `objectid`, `geoname`, `county`, `nad83_lat`, and `nad83_lon`.
- Pagination response includes `count`, `next`, `previous`, and `results`.

---
