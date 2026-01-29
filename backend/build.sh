#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "🗃️  Collecting static files..."
python manage.py collectstatic --no-input

echo "🔄 Running migrations..."
python manage.py migrate

echo "👤 Creating admin and test users..."
python create_role_users.py || echo "⚠️  Users may already exist"

echo "✅ Build complete!"
