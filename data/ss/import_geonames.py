import psycopg
import csv
from decouple import config

def import_data(csv_file):
    """
    Import data from a CSV file into the PostgreSQL database using Psycopg 3,
    creating the table if it doesn't exist, replacing existing data,
    and using environment variables from a .env file.
    """
    try:
        with psycopg.connect(
            dbname=config("POSTGRES_DB"),
            user=config("POSTGRES_USER"),
            password=config("POSTGRES_PASSWORD"),
            host=config("POSTGRES_HOST"), # Use config for host, with a default
            port=config("POSTGRES_PORT")
        ) as conn:
            with conn.cursor() as cur:
                # Check if the table exists
                cur.execute("SELECT to_regclass('public.origin');")
                table_exists = cur.fetchone()[0]

                if not table_exists:
                    # Create the table if it doesn't exist
                    cur.execute("""
                        CREATE TABLE origin (
                            objectid integer,
                            cgndb_key text,
                            geoname text,
                            county text,
                            nad83_lat float,
                            nad83_lon float
                            
                        );
                    """)
                    print("Table 'origin' created.")

                    # Open the CSV file and read its contents
                    with open(csv_file, 'r') as f:
                        reader = csv.reader(f)
                        next(reader)  # Skip the header row

                        # Insert rows from the CSV file into the database
                        for row in reader:
                            cur.execute("""
                                INSERT INTO origin (objectid,cgndb_key,geoname,county,nad83_lat,nad83_lon)
                                VALUES (%s, %s, %s, %s, %s, %s);
                            """, row)

                        # Commit the transaction to save changes in the database
                        conn.commit()
                        print("Origin Data imported successfully.")
                else:
                    # Delete the Table Logic
                    # Delete existing data if the table exists
                    #cur.execute("DELETE FROM origin;")
                    #print("Existing data in 'origin' deleted.")
                    print("Table Exists")

    except psycopg.Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import_data('./data/Nova_Scotia_GeoNAMES.csv')