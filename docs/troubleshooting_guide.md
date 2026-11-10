#### 1. Enable Hot-Reloading (Essential for Dev)

Currently, your Python code is baked into the image during the build. If you change a line of code in a Django view, you have to rebuild the container to see the change.

* **Recommendation:** Mount your current directory to the container's working directory.
* **Action:** Add `- .:/usr/src/app` to your `volumes`.

#### 2. Network Isolation

By default, all containers are on the same bridge network, but it’s best practice to explicitly define a backend network. This prevents external traffic from accidentally hitting your DB and keeps the "Transit Network" internal logic isolated.

* **Recommendation:** Add a bridge network called `cptn_network`.

#### 3. Log Management

Django and Postgres can generate a lot of logs during GTFS imports. Without a cap, these logs can eventually fill up the student's disk space on their WSL2 instance.

* **Recommendation:** Add a `logging` driver to cap log sizes.

---

### 🎓 Instructor Insight: Why `PYTHONUNBUFFERED: 1`?

In Docker, Python sometimes buffers logs, meaning if the app crashes, the last few (and most important) lines of the traceback might not show up in `docker logs` immediately. Setting this to `1` ensures that the `cptn_api` logs are streamed in real-time, which is crucial for students troubleshooting their API logic.

### 🧪 Verification Check

Once you run `make up`, you can verify the GIS libraries are actually linked by running this command:

```bash
docker exec -it cptn_api python manage.py shell -c "from django.contrib.gis.geos import libgeos; print(libgeos.geos_version())"

```

### 🚀 What to do now

1. **Create the migrations** (now that the code is valid):
```bash
docker exec -it cptn_api python manage.py makemigrations

```

2. **Run the migrations** (now that the code is valid):
```bash
docker exec -it cptn_api python manage.py migrate

```

3. **Check the API logs** to ensure the development server has started:
```bash
docker logs -f cptn_api

```

```bash
docker-compose exec db psql -U cptn_user -d cptn_db
```

```bash
DROP TABLE journey_shapes CASCADE;
\q
```

If the `web` container isn't running, you can't use `exec` because `exec` requires an active process to "hook" into. 

Instead, use **`docker-compose run`**. This starts a new, temporary container specifically to run the command and then shuts it down automatically.

### 🛠️ The Alternative Command
Run this from your project root:

```bash
docker-compose run --rm web python manage.py migrate journey 0002 --fake
```

---

### 🔄 The Full Recovery Sequence
Since you are in the middle of fixing that `multiple primary keys` error, here is the full "no-server-running" sequence:

1.  **Start just the Database:**
    `docker-compose up -d db`
2.  **Drop the bad table (via a temp container):**
    `docker-compose run --rm db psql -h db -U [USER] -d [DB_NAME] -c "DROP TABLE journey_shapes CASCADE;"`
    `docker-compose run --rm db psql -h db -U cptn_user -d cptn_db -c "DROP TABLE journey_shapes CASCADE;"`
3.  **Fake the rollback:**
    `docker-compose run --rm web python manage.py migrate journey 0002 --fake`
4.  **Apply the fix for real:**
    `docker-compose run --rm web python manage.py migrate`
5.  **Start everything back up:**
    `docker-compose up -d`


Since you're using **PostGIS** under the hood, pgAdmin has a built-in "Geometry Viewer" that is perfect for this. It’s much more satisfying than looking at raw coordinates because it actually plots your GeoNames and campuses on an OpenStreetMap layer.

Open the **Query Tool** in pgAdmin and run this script:

```sql
-- 1. Check for any 'orphaned' Areas (missing spatial data)
SELECT area_id, area_name, county 
FROM journey_area 
WHERE location IS NULL;

-- 2. Visualize all Areas and their validity
-- Note: In pgAdmin, click the "Eye" icon in the 'location' column header to see the map!
SELECT 
    area_id, 
    area_name, 
    ST_AsText(location) AS wkt_geometry, -- Human readable text
    ST_IsValid(location) AS is_valid,    -- Check if the point is mathematically sound
    location                            -- The actual geometry for the Map Viewer
FROM journey_area;

```

### 🗺️ Using the Geometry Viewer

Once you run the second query, look at the results grid.

1. In the column named `location`, you will see a small **Eye icon** in the header or next to the data.
2. Click it.
3. A new panel will open showing **Nova Scotia**. Your imported areas should appear as blue dots. If you zoom in on Port Hawkesbury, you should see the clusters you just seeded.

---

### 🎓 Instructor Tip: The "Health Check" Query

If you want to make sure your `StopArea` linking logic actually worked, run this join. It will show you exactly which campus "claims" which geographic areas:

```sql
SELECT 
    s.stop_name, 
    a.area_name, 
    a.county,
    ST_Distance(s.location, a.location) / 1000 AS distance_km
FROM journey_stoparea sa
JOIN journey_stops s ON sa.stop_id = s.stop_id
JOIN journey_area a ON sa.area_id = a.area_id
ORDER BY s.stop_name, distance_km;

```
