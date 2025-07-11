#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# --- ADD THIS LINE ---
# This command finds and loads the initial_data.json fixture.
python manage.py loaddata initial_data.json