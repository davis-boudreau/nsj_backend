### 🚀 How to Run the Importer

Place your CSV files in the `data/` directory of your project, then run the following inside your Docker container:

```bash
docker exec -it cptn_api python manage.py import_cptn_data \
  --stops data/stops.csv \
  --areas data/geonames.csv \
  --dist 2

```
