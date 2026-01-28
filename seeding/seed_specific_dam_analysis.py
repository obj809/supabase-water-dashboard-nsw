# seeding/seed_specific_dam_analysis.py

import datetime as dt

from db import get_connection


def last_day_prev_month() -> str:
    first_of_this_month = dt.date.today().replace(day=1)
    last_of_prev = first_of_this_month - dt.timedelta(days=1)
    return last_of_prev.isoformat()


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def main() -> None:
    analysis_date = last_day_prev_month()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT dam_id, COALESCE(full_volume, 0) FROM dams ORDER BY dam_id;")
    dams = cur.fetchall()

    if not dams:
        print("seed_specific_dam_analysis.py: No dams found. Seed 'dams' first.")
        cur.close()
        conn.close()
        return

    rows = []
    for i, (dam_id, full_vol) in enumerate(dams):
        full_vol_int = int(full_vol) if full_vol is not None else 0
        capacity = full_vol_int if full_vol_int > 0 else (200_000 + 10_000 * i)

        wiggle = (i % 6) * 0.002

        v12 = round(capacity * (0.96 + wiggle), 3)
        v5 = round(capacity * (0.94 + wiggle), 3)
        v20 = round(capacity * (0.92 + wiggle), 3)

        p12 = clamp(96 - (i % 5), 85, 100)
        p5 = clamp(94 - (i % 5), 85, 100)
        p20 = clamp(92 - (i % 5), 85, 100)

        inflow12 = 1200 + 50 * i
        inflow5 = round(inflow12 * 0.97, 3)
        inflow20 = round(inflow12 * 0.94, 3)

        release12 = round(inflow12 * 0.70, 3)
        release5 = round(inflow5 * 0.70, 3)
        release20 = round(inflow20 * 0.70, 3)

        rows.append(
            (
                dam_id,
                analysis_date,
                v12,
                v5,
                v20,
                float(p12),
                float(p5),
                float(p20),
                float(inflow12),
                float(inflow5),
                float(inflow20),
                float(release12),
                float(release5),
                float(release20),
            )
        )

    sql = """
    INSERT INTO specific_dam_analysis (
        dam_id, analysis_date,
        avg_storage_volume_12_months, avg_storage_volume_5_years, avg_storage_volume_20_years,
        avg_percentage_full_12_months, avg_percentage_full_5_years, avg_percentage_full_20_years,
        avg_storage_inflow_12_months, avg_storage_inflow_5_years, avg_storage_inflow_20_years,
        avg_storage_release_12_months, avg_storage_release_5_years, avg_storage_release_20_years
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (dam_id, analysis_date) DO UPDATE SET
        avg_storage_volume_12_months = EXCLUDED.avg_storage_volume_12_months,
        avg_storage_volume_5_years = EXCLUDED.avg_storage_volume_5_years,
        avg_storage_volume_20_years = EXCLUDED.avg_storage_volume_20_years,
        avg_percentage_full_12_months = EXCLUDED.avg_percentage_full_12_months,
        avg_percentage_full_5_years = EXCLUDED.avg_percentage_full_5_years,
        avg_percentage_full_20_years = EXCLUDED.avg_percentage_full_20_years,
        avg_storage_inflow_12_months = EXCLUDED.avg_storage_inflow_12_months,
        avg_storage_inflow_5_years = EXCLUDED.avg_storage_inflow_5_years,
        avg_storage_inflow_20_years = EXCLUDED.avg_storage_inflow_20_years,
        avg_storage_release_12_months = EXCLUDED.avg_storage_release_12_months,
        avg_storage_release_5_years = EXCLUDED.avg_storage_release_5_years,
        avg_storage_release_20_years = EXCLUDED.avg_storage_release_20_years;
    """

    cur.executemany(sql, rows)
    conn.commit()

    print(
        f"seed_specific_dam_analysis.py: upserted {len(rows)} row(s) for {len(rows)} dam(s) on {analysis_date}."
    )
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
