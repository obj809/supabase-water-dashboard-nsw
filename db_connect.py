# db_connect.py

import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")

def build_url_from_parts():
    user = os.getenv("SUPABASE_DB_USER")
    password = os.getenv("SUPABASE_DB_PASSWORD")
    host = os.getenv("SUPABASE_DB_HOST")
    dbname = os.getenv("SUPABASE_DB_NAME")

    if not all([user, password, host, dbname]):
        raise RuntimeError("Missing atomic DB env vars")

    password = quote_plus(password)

    return f"postgresql://{user}:{password}@{host}/{dbname}"

def get_connection():
    url = DATABASE_URL or build_url_from_parts()
    return psycopg2.connect(url)

if __name__ == "__main__":
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            print("✅ Connected:", cur.fetchone())
