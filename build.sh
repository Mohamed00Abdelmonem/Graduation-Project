#!/bin/bash

# Install dependencies with explicit psycopg2-binary first
echo "Installing dependencies..."
python3.12 -m pip install psycopg2-binary==2.9.9
python3.12 -m pip install -r requirements.txt

# Database migrations
echo "Running migrations..."
python3.12 manage.py makemigrations --noinput
python3.12 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear