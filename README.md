# Supabase Water Dashboard NSW

A Supabase PostgreSQL-based system for tracking and analyzing dam data across NSW, Australia. Built with Python and psycopg2.

## Table of Contents

- [Goals & MVP](#goals--mvp)
- [Tech Stack](#tech-stack)
- [How To Use](#how-to-use)
- [Design Goals](#design-goals)
- [Project Features](#project-features)
- [Project Structure](#project-structure)
- [Additions & Improvements](#additions--improvements)
- [Learning Highlights](#learning-highlights)
- [Known Issues](#known-issues)
- [Challenges](#challenges)
- [Contact](#contact)

## Goals & MVP

> "Create a cloud-hosted system that stores dam metadata, tracks water storage levels, archives historical data, and generates analytical reports with rolling averages (12-month, 5-year, 20-year) for 36 NSW dams."

## Tech Stack

- Python 3
- PostgreSQL (Supabase)
- psycopg2-binary
- python-dateutil
- python-dotenv

## How To Use

1. Create virtual environment: `python3 -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with Supabase credentials (see `example.env`)
4. Run database setup: `python scripts/db_connect.py && python scripts/create_schema.py && python scripts/seed_data.py`
5. Verify data: `python scripts/verify_seed.py`

## Design Goals

- **Cloud-Native**: Hosted on Supabase PostgreSQL for accessibility
- **Data Integrity**: Foreign keys with cascading relationships
- **Idempotency**: Upsert operations for safe re-runs
- **Security**: Parameterized queries to prevent SQL injection
- **Modularity**: Separate seeding scripts with dependency-ordered execution

## Project Features

- 36 NSW dams with metadata (capacity, coordinates, identifiers)
- Dam grouping system (Sydney, popular, large, small, greatest released)
- 24-month historical snapshots with time-series data
- Per-dam and system-wide rolling average analysis (12-month, 5-year, 20-year)

## Project Structure

```
supabase-water-dashboard-nsw/
├── scripts/
│   ├── db_connect.py                # Test database connectivity
│   ├── create_schema.py             # Initialize database schema
│   ├── seed_data.py                 # Run all seeders in sequence
│   └── verify_seed.py               # Verify seeded data
├── seeding/
│   ├── db.py                        # Centralized database connection
│   ├── seed_dams.py                 # Seed 36 NSW dams
│   ├── seed_dam_groups.py           # Seed 5 dam groups
│   ├── seed_dam_group_members.py    # Seed dam-group mappings
│   ├── seed_dam_resources.py        # Seed 24-month historical data
│   ├── seed_latest_data.py          # Seed current snapshot
│   ├── seed_specific_dam_analysis.py
│   └── seed_overall_dam_analysis.py
├── example.env
├── requirements.txt
└── schema.sql
```

## Additions & Improvements

- [ ] Dashboard visualization layer
- [ ] Automated data refresh scheduling
- [ ] Real-time data integration with WaterNSW API
- [ ] Multi-region support

## Learning Highlights

- Normalized database schema design with foreign key relationships
- Cloud PostgreSQL deployment with Supabase
- Orchestrated data pipelines with dependency ordering
- Upsert patterns and composite primary keys in PostgreSQL

## Known Issues

- Synthetic data; does not reflect actual NSW dam levels
- Manual refresh required; no automated scheduling
- Analysis calculations use fixed values

## Challenges

- Establishing correct seeding order for foreign key constraints
- Designing composite primary keys for analysis tables
- Generating realistic synthetic historical data patterns

## Contact Me
- Visit my [LinkedIn](https://www.linkedin.com/in/obj809/) for more details.
- Check out my [GitHub](https://github.com/cyberforge1) for more projects.
- Or send me an email at obj809@gmail.com
<br />
Thanks for your interest in this project. Feel free to reach out with any thoughts or questions.
<br />
<br />
Oliver Jenkins © 2025
