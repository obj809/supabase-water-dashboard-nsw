# seed_data.py

import os
import sys
import subprocess
from typing import List

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

SEEDING_SCRIPTS: List[str] = [
    "seeding/seed_dams.py",
    "seeding/seed_dam_groups.py",
    "seeding/seed_dam_group_members.py",
    "seeding/seed_dam_resources.py",
    "seeding/seed_latest_data.py",
    "seeding/seed_specific_dam_analysis.py",
    "seeding/seed_overall_dam_analysis.py",
]

def root_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))

def main() -> None:
    if load_dotenv:
        env_path = os.path.join(root_dir(), ".env")
        if os.path.exists(env_path):
            load_dotenv(env_path)

    db_url = os.getenv("SUPABASE_DATABASE_URL", "(unknown)")
    print(f"Target database URL: {db_url}")

    for rel_path in SEEDING_SCRIPTS:
        full_path = os.path.join(root_dir(), rel_path)
        if not os.path.isfile(full_path):
            print(f"Missing script: {rel_path}")
            sys.exit(1)

        print(f"\nRunning {rel_path}")
        result = subprocess.run(
            [sys.executable, full_path],
            cwd=root_dir(),
        )

        if result.returncode != 0:
            print(f"{rel_path} failed with exit code {result.returncode}")
            sys.exit(result.returncode)

    print("\nSeeding completed successfully.")

if __name__ == "__main__":
    main()
