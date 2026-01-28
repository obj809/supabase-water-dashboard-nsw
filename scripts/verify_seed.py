# verify_seed.py

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("SUPABASE_DATABASE_URL")
if not DB_URL:
    raise RuntimeError("SUPABASE_DATABASE_URL not set")

TABLES = [
    "dams",
    "dam_groups",
    "dam_group_members",
    "dam_resources",
    "latest_data",
    "specific_dam_analysis",
    "overall_dam_analysis",
]


def main() -> None:
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            for table in TABLES:
                cur.execute(f"SELECT COUNT(*) FROM {table};")
                count = cur.fetchone()[0]

                cur.execute(f"SELECT * FROM {table} LIMIT 3;")
                rows = cur.fetchall()
                col_names = [desc[0] for desc in cur.description]

                print(f"\n{'=' * 60}")
                print(f"TABLE: {table} ({count} rows)")
                print(f"{'=' * 60}")
                print(f"Columns: {', '.join(col_names)}")
                print("-" * 60)

                for row in rows:
                    print(row)

                if not rows:
                    print("(empty)")


if __name__ == "__main__":
    main()
