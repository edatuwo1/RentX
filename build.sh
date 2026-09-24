#!/usr/bin/env bash

# NOTE: Install the Python packages required by RentX.
pip install -r requirements.txt

# NOTE: Collect Django's static files for production.
python manage.py collectstatic --noinput

# NOTE: Apply database migrations before RentX starts.
python manage.py migrate