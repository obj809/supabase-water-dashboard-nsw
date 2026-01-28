# commands.md

## create venv

python3 -m venv venv

## activate venv

source venv/bin/activate

## freeze requirements

pip freeze > requirements.txt

## install dependencies

pip install -r requirements.txt

## run main

python scripts/db_connect.py

python scripts/create_schema.py

python scripts/seed_data.py

python scripts/verify_seed.py