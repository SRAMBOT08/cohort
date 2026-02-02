#!/bin/bash
set -e

echo "Installing backend dependencies"
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "Building frontend"
npm install
npm run build

echo "Frontend built directly to backend/static/frontend"

echo "Collect Django static files"
cd backend
python manage.py collectstatic --noinput

echo "Running migrations"
python manage.py migrate --noinput

echo "Build completed successfully!"
