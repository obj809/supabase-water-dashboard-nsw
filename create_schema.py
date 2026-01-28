# create_schema.py

import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("SUPABASE_DATABASE_URL")
if not DB_URL:
    raise RuntimeError("SUPABASE_DATABASE_URL not set")

ROOT_DIR = Path(__file__).resolve().parent
SCHEMA_FILE = ROOT_DIR / "schema.sql"

if not SCHEMA_FILE.exists():
    raise FileNotFoundError(f"schema.sql not found at {SCHEMA_FILE}")

def main() -> None:
    print("Connecting to Supabase Postgres...")
    schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")

    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(schema_sql)
            conn.commit()
        print("Schema applied successfully.")
    except Exception as e:
        print("Failed to apply schema.")
        raise e

if __name__ == "__main__":
    main()
