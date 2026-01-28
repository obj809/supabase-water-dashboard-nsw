# seeding/seed_dam_group_members.py

from psycopg2.extras import execute_values
from seeding.db import get_connection

MEMBERS = [
    ("sydney_dams","212232"), ("sydney_dams","212220"), ("sydney_dams","212211"),
    ("sydney_dams","212205"), ("sydney_dams","213210"), ("sydney_dams","213240"),
    ("sydney_dams","212212"), ("sydney_dams","215235"),
    ("popular_dams","212243"), ("popular_dams","212232"), ("popular_dams","212220"),
    ("popular_dams","212211"), ("popular_dams","212205"), ("popular_dams","213210"),
    ("popular_dams","215212"), ("popular_dams","213240"),
    ("large_dams","212243"), ("large_dams","410102"), ("large_dams","412010"),
    ("large_dams","418035"), ("large_dams","410131"), ("large_dams","421078"),
    ("large_dams","210097"), ("large_dams","419080"),
    ("small_dams","219033"), ("small_dams","215235"), ("small_dams","215212"),
    ("small_dams","42510037"), ("small_dams","219027"), ("small_dams","203042"),
    ("small_dams","210102"), ("small_dams","412107"),
    ("greatest_released","410102"), ("greatest_released","410131"),
    ("greatest_released","421078"), ("greatest_released","418035"),
    ("greatest_released","210117"), ("greatest_released","210097"),
    ("greatest_released","419041"), ("greatest_released","412010"),
]

SQL = """
INSERT INTO dam_group_members (group_name, dam_id)
VALUES %s
ON CONFLICT (group_name, dam_id) DO UPDATE
SET group_name = EXCLUDED.group_name,
    dam_id = EXCLUDED.dam_id;
"""

def main() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, SQL, MEMBERS)
        conn.commit()

    print(f"seed_dam_group_members.py: upserted {len(MEMBERS)} rows")

if __name__ == "__main__":
    main()
