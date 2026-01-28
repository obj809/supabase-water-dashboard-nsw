# seeding/seed_latest_data.py

import datetime as dt

from psycopg2.extras import execute_values

from db import get_connection


SQL = """
INSERT INTO latest_data
  (dam_id, dam_name, date, storage_volume, percentage_full, storage_inflow, storage_release)
VALUES %s
ON CONFLICT (dam_id) DO UPDATE SET
  dam_name = EXCLUDED.dam_name,
  date = EXCLUDED.date,
  storage_volume = EXCLUDED.storage_volume,
  percentage_full = EXCLUDED.percentage_full,
  storage_inflow = EXCLUDED.storage_inflow,
  storage_release = EXCLUDED.storage_release;
"""


def main() -> None:
    today = dt.date.today().isoformat()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT dam_id, dam_name, COALESCE(full_volume, 0) FROM dams ORDER BY dam_id;"
            )
            dams = cur.fetchall()

            if not dams:
                print("seed_latest_data.py: No dams found. Seed 'dams' first.")
                return

            rows: list[tuple] = []
            for i, (dam_id, dam_name, full_volume) in enumerate(dams):
                pct = 92 + (i % 9)
                inflow = 1000 + 100 * i
                release = round(inflow * 0.70, 3)

                full_vol_int = int(full_volume) if full_volume is not None else 0
                cap = full_vol_int if full_vol_int > 0 else (200_000 + 10_000 * i)
                storage = round(cap * (pct / 100.0), 3)

                rows.append((dam_id, dam_name, today, storage, float(pct), float(inflow), release))

            execute_values(cur, SQL, rows)
        conn.commit()

    print(f"seed_latest_data.py: upserted {len(rows)} row(s) for {len(rows)} dam(s).")


if __name__ == "__main__":
    main()
