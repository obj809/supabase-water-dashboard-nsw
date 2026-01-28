# seeding/seed_dam_resources.py

import datetime as dt

from dateutil.relativedelta import relativedelta
from psycopg2.extras import execute_values

from seeding.db import get_connection


def month_starts(n_months: int = 24) -> list[str]:
    today = dt.date.today().replace(day=1)
    months = [(today - relativedelta(months=i)) for i in range(n_months, 0, -1)]
    return [d.isoformat() for d in months]


def main() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT dam_id, COALESCE(full_volume, 0) FROM dams ORDER BY dam_id;")
            dams = cur.fetchall()

            if not dams:
                print("seed_dam_resources.py: No dams found. Seed 'dams' first.")
                return

            dates = month_starts(24)
            start_date = dates[0]
            end_date = dates[-1]

            delete_sql = """
            DELETE FROM dam_resources
            WHERE dam_id = %s AND date BETWEEN %s AND %s;
            """

            for (dam_id, _) in dams:
                cur.execute(delete_sql, (dam_id, start_date, end_date))

            rows: list[tuple] = []
            for i, (dam_id, full_vol) in enumerate(dams):
                full_vol_int = int(full_vol) if full_vol is not None else 0
                capacity = full_vol_int if full_vol_int > 0 else (200_000 + 10_000 * i)

                base_pct = 90.0 + ((i % 20) * 0.5)
                for m, d in enumerate(dates):
                    pct = min(100.0, max(60.0, base_pct + ((m % 12) - 6) * 0.35))
                    storage = round(capacity * (pct / 100.0), 3)
                    inflow = round(900 + (i * 15) + (m * 20), 3)
                    release = round(inflow * 0.7, 3)
                    rows.append((dam_id, d, storage, pct, inflow, release))

            insert_sql = """
            INSERT INTO dam_resources
              (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release)
            VALUES %s;
            """

            execute_values(cur, insert_sql, rows)
        conn.commit()

    print(
        f"seed_dam_resources.py: inserted {len(rows)} rows across {len(dams)} dams x {len(dates)} months."
    )


if __name__ == "__main__":
    main()
