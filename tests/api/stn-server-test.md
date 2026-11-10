### Student transit Network API Server Testing Procedure

#### Objective
To verify the functionality and response accuracy of the OpenRouteService API and the STN API for retrieving driving directions between specified coordinates.

#### Overview
The STN API returns GeoJSON from OpenRouteService with closest stops along the route.  
The stops are retrieved from the GTFS Static Feed Table Stops in the STN Database.

#### Tools Required
- **cURL**: Command-line tool for transferring data with URLs.
- **API Key**: Valid API key for OpenRouteService.  
- **Local Server**: Running instance of the STN API.

#### Test Cases

1. **OpenRouteService API**
   - **Endpoint**: `https://api.openrouteservice.org/v2/directions/driving-car`
   - **Method**: GET
   - **Parameters**:
     - `api_key`: Your API key.
     - `start`: Starting coordinates (`-61.991581,45.622765`).
     - `end`: Ending coordinates (`-61.3696801,45.6270521`).

   **Steps**:
   1. Open terminal.
   2. Execute the following cURL command:
      ```sh
      curl -X GET "https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248597ab31ae19e4da99a06d24b3869a54b&start=-61.991581,45.622765&end=-61.3696801,45.6270521"
      ```
      or
      ```sh
      https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248597ab31ae19e4da99a06d24b3869a54b&start=-61.991581,45.622765&end=-61.3696801,45.6270521
      ```
   3. Verify the response contains valid route information, including distance, duration, and waypoints.  When using a web browser, use pretty format.

2. **STN API**
   - **Endpoint**: `http://localhost:8000/api/v1/stn/GetGeoRoutes`
   - **Method**: GET
   - **Parameters**:
     - `start_lon`: Starting longitude (`-61.991581`).
     - `start_lat`: Starting latitude (`45.622765`).
     - `end_lon`: Ending longitude (`-61.3696801`).
     - `end_lat`: Ending latitude (`45.6270521`).

   **Steps**:
   1. Ensure the local server is running.
   2. Open terminal.
   3. Execute the following cURL command:
      ```sh
      curl -X GET "http://localhost:8000/api/v1/stn/GetGeoRoutes?start_lon=-61.991581&start_lat=45.622765&end_lon=-61.3696801&end_lat=45.6270521"
      ```
      or
      ```sh
      http://localhost:8000/api/v1/stn/GetGeoRoutes?start_lon=-61.991581&start_lat=45.622765&end_lon=-61.3696801&end_lat=45.6270521
      ```
   4. Verify the response contains valid route information, including distance, duration, waypoints clostest stops.  When using a web browser, use pretty format.

#### Expected Results
- Both APIs should return a JSON response with accurate route details.
- The responses should include key information such as distance, estimated travel time, and route geometry.  In addition the GetGeoRoutes API endpoint returns closest stops.

#### Notes
- Ensure the API key for OpenRouteService is valid and has sufficient quota.
- The key in the samples belong to davis.boudreau@nscc.ca.
- Confirm the local server for STN API is properly configured and running.

