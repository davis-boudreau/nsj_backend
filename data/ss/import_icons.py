import csv
import psycopg
from decouple import config


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS icons (
    icon_id TEXT PRIMARY KEY,
    icon_name TEXT UNIQUE,
    icon_path TEXT
);
"""

UPSERT_SQL = """
INSERT INTO icons (icon_id, icon_name, icon_path)
VALUES (%(icon_id)s, %(icon_name)s, %(icon_path)s)
ON CONFLICT (icon_id) DO UPDATE SET
    icon_name = EXCLUDED.icon_name,
    icon_path = EXCLUDED.icon_path;
"""


def _clean(s):
    if s is None:
        return None
    s = str(s).strip()
    return s if s != "" else None


def _normalize_icon_path(icon_path: str) -> str:
    """
    Normalize icon_path to be relative to Django static root:
      "/icons/x.png" -> "icons/x.png"
      "icons/x.png"  -> "icons/x.png"
      "x.png"        -> "icons/x.png"
    """
    icon_path = _clean(icon_path) or ""
    if not icon_path:
        return icon_path

    # Remove leading slash if present
    if icon_path.startswith("/"):
        icon_path = icon_path[1:]

    # If it's just a filename, place it under icons/
    if "/" not in icon_path:
        icon_path = f"icons/{icon_path}"

    return icon_path

def import_data(csv_file: str) -> None:
    conninfo = dict(
        dbname=config("POSTGRES_DB"),
        user=config("POSTGRES_USER"),
        password=config("POSTGRES_PASSWORD"),
        host=config("POSTGRES_HOST"),
        port=config("POSTGRES_PORT"),
    )

    with psycopg.connect(**conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)

            with open(csv_file, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                row_count = 0
                skipped = 0

                for row in reader:
                    icon_id = _clean(row.get("icon_id"))
                    icon_name = _clean(row.get("icon_name"))
                    icon_path = _normalize_icon_path(row.get("icon_path"))

                    if not icon_id or not icon_name or not icon_path:
                        skipped += 1
                        continue

                    cur.execute(
                        UPSERT_SQL,
                        {"icon_id": icon_id, "icon_name": icon_name, "icon_path": icon_path},
                    )
                    row_count += 1

            conn.commit()
            print(f"Icons import complete. Upserted {row_count} rows. Skipped {skipped} rows.")


if __name__ == "__main__":
    import_data("./data/icons.csv")
