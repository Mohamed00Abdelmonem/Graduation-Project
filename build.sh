#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
python3.12 -m pip install -r requirements.txt

# Database migrations
echo "Running migrations..."
python3.12 manage.py makemigrations --noinput
python3.12 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear

# Create vercel.json if not exists
if [ ! -f vercel.json ]; then
  echo "Creating vercel.json..."
  cat > vercel.json <<EOL
{
  "version": 2,
  "builds": [
    {
      "src": "project/wsgi.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.12"
      }
    },
    {
      "src": "staticfiles/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/media/(.*)",
      "dest": "/media/$1"
    },
    {
      "src": "/(.*)",
      "dest": "project/wsgi.py"
    }
  ]
}
EOL
fi