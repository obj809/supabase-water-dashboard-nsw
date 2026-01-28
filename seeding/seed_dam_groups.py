# seeding/seed_dam_groups.py

from psycopg2.extras import execute_values
from db import get_connection

GROUPS = [
    ("sydney_dams",),
    ("popular_dams",),
    ("large_dams",),
    ("small_dams",),
    ("greatest_released",),
]

SQL = """
INSERT INTO dam_groups (group_name)
VALUES %s
ON CONFLICT (group_name) DO UPDATE
SET group_name = EXCLUDED.group_name;
"""

def main() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, SQL, GROUPS)
        conn.commit()

    print(f"seed_dam_groups.py: upserted {len(GROUPS)} rows")

if __name__ == "__main__":
    main()
