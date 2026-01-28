# seeding/db.py

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_URL = os.getenv("SUPABASE_DATABASE_URL")
if not DB_URL:
    raise RuntimeError("SUPABASE_DATABASE_URL not set")

def get_connection():
    return psycopg2.connect(DB_URL)
