#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Run Django's 'check' command to find potential problems
python manage.py check --deploy

# Collect static files into the STATIC_ROOT directory
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
