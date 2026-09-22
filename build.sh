#!/usr/bin/env bash

# NOTE: Collect Django's static files for production.
python manage.py collectstatic --noinput

# NOTE: Apply any database migrations before the application starts.
python manage.py migrate