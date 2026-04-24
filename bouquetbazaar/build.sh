#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from the requirements file in the parent directory
pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
