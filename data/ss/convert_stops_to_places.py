import csv
from pathlib import Path

INPUT = Path("./data/stops.csv")
OUTPUT = Path("./data/places.csv")

def norm(s) -> str:
    return (s or "").strip()

def normalize_icon_path(icon_value: str) -> str:
    v = norm(icon_value).replace("\\", "/").lstrip("/")
    if not v:
        return ""
    if v.startswith("icons/"):
        return v
    filename = v.split("/")[-1]
    return f"icons/{filename}"

def categorize(place_name: str) -> str:
    name = norm(place_name).lower()

    school_keywords = [
        "nscc", "university", "college", "université", "universite", "nscad",
        "dalhousie", "saint mary", "st. mary", "st mary",
        "st. francis xavier", "st francis xavier", "acadia",
        "cape breton", "coast guard", "gaelic college",
    ]
    if any(k in name for k in school_keywords):
        return "SCHOOL"

    if "car pool" in name or "carpool" in name:
        return "CARPOOL"

    sponsor_keywords = [
        "give/get-a-ride",
        "tim horton's", "tim hortons", "superstore",
        "inn", "career college", "business college", "academy",
        "firefighters", "spca", "futureworx", "peopleworx",
        "medavie", "conservatory", "flight attendant",
        "massage", "hydrotherapy", "truck training", "beauty institute",
        "environmental training", "distance education", "hair",
        "cosmetology", "acupuncture", "traditional chinese medicine",
        "police", "training centre", "training center",
        "eastern college", "oxford international", "academy of learning",
        "canadian college", "dexter institute", "building trades",
    ]
    if any(k in name for k in sponsor_keywords):
        return "SPONSOR"

    return "MEET_POINT"

def convert():
    if not INPUT.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT}")

    with INPUT.open("r", encoding="utf-8-sig", newline="") as f_in, OUTPUT.open("w", encoding="utf-8", newline="") as f_out:
        reader = csv.DictReader(f_in)

        # Normalize headers: strip + lowercase
        raw_fields = reader.fieldnames or []
        keymap = {norm(h).lower(): h for h in raw_fields}

        def get(row, key):
            """Get a value by normalized header name."""
            original = keymap.get(key.lower())
            return row.get(original) if original else None

        fieldnames = [
            "place_id","place_name","place_desc","place_lat","place_lon",
            "zone_id","place_url","place_icon","place_category"
        ]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        skipped_blank = 0

        for row in reader:
            stop_id = norm(get(row, "stop_id"))
            if not stop_id:
                skipped_blank += 1
                continue  # ✅ prevents PK '' duplicates

            stop_name = norm(get(row, "stop_name"))
            stop_desc = norm(get(row, "stop_desc"))
            stop_lat  = norm(get(row, "stop_lat"))
            stop_lon  = norm(get(row, "stop_lon"))
            zone_id   = norm(get(row, "zone_id"))
            stop_url  = norm(get(row, "stop_url"))
            stop_icon = norm(get(row, "stop_icon"))

            writer.writerow({
                "place_id": stop_id,
                "place_name": stop_name,
                "place_desc": stop_desc,
                "place_lat": stop_lat,
                "place_lon": stop_lon,
                "zone_id": zone_id,
                "place_url": stop_url,
                "place_icon": normalize_icon_path(stop_icon),
                "place_category": categorize(stop_name),
            })

    print(f"✅ Created: {OUTPUT} from {INPUT}")
    if skipped_blank:
        print(f"⚠️ Skipped {skipped_blank} row(s) with blank stop_id")

if __name__ == "__main__":
    convert()
