import psycopg
import csv
from decouple import config

def import_data(csv_file):
    with psycopg.connect(
        dbname=config("POSTGRES_DB"),
        user=config("POSTGRES_USER"),
        password=config("POSTGRES_PASSWORD"),
        host=config("POSTGRES_HOST"),
        port=config("POSTGRES_PORT"),
    ) as conn:
        with conn.cursor() as cur:
            # Ensure table exists with the columns you now expect
            cur.execute("""
                CREATE TABLE IF NOT EXISTS stops (
                    stop_id TEXT PRIMARY KEY,
                    stop_name TEXT,
                    stop_desc TEXT,
                    stop_lat DOUBLE PRECISION,
                    stop_lon DOUBLE PRECISION,
                    zone_id INTEGER,
                    stop_url TEXT,
                    stop_icon TEXT,
                    agency_id TEXT NULL,
                    is_public BOOLEAN DEFAULT TRUE,
                    stop_category TEXT DEFAULT 'MEET_POINT'
                );
            """)

            # Replace existing data
            cur.execute("DELETE FROM stops;")
            print("Existing data cleared from 'stops'.")

            seen = set()

            with open(csv_file, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                for raw in reader:
                    stop_id = (raw.get("stop_id") or "").strip()

                    # ✅ Skip bad rows
                    if not stop_id:
                        continue

                    # ✅ Optional: skip duplicates inside the CSV
                    if stop_id in seen:
                        continue
                    seen.add(stop_id)

                    stop_name = (raw.get("stop_name") or "").strip()
                    stop_desc = (raw.get("stop_desc") or "").strip()
                    stop_lat  = (raw.get("stop_lat") or "").strip()
                    stop_lon  = (raw.get("stop_lon") or "").strip()
                    zone_id   = (raw.get("zone_id") or "").strip()
                    stop_url  = (raw.get("stop_url") or "").strip()
                    stop_icon = (raw.get("stop_icon") or "").strip()

                    # Default category (you said “go with the defaults”)
                    stop_category = (raw.get("stop_category") or "MEET_POINT").strip() or "MEET_POINT"

                    cur.execute("""
                        INSERT INTO stops (
                            stop_id, stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, stop_icon,
                            agency_id, is_public, stop_category
                        )
                        VALUES (
                            %s, %s, NULLIF(%s,''), NULLIF(%s,'')::double precision, NULLIF(%s,'')::double precision,
                            NULLIF(%s,'')::integer, NULLIF(%s,''), NULLIF(%s,''),
                            NULL, TRUE, %s
                        )
                        ON CONFLICT (stop_id) DO UPDATE SET
                            stop_name = EXCLUDED.stop_name,
                            stop_desc = EXCLUDED.stop_desc,
                            stop_lat = EXCLUDED.stop_lat,
                            stop_lon = EXCLUDED.stop_lon,
                            zone_id = EXCLUDED.zone_id,
                            stop_url = EXCLUDED.stop_url,
                            stop_icon = EXCLUDED.stop_icon,
                            stop_category = EXCLUDED.stop_category;
                    """, (
                        stop_id, stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, stop_icon, stop_category
                    ))

            conn.commit()
            print("Places imported successfully.")

if __name__ == "__main__":
    import_data("./data/places.csv")
