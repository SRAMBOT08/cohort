#!/usr/bin/env bash
# exit on error
set -o errexit

echo "========================================="
echo "🚀 Starting Build Process"
echo "========================================="

echo ""
echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🗃️  Collecting static files..."
python manage.py collectstatic --no-input

echo ""
echo "🔄 Running migrations..."
python manage.py migrate

echo ""
echo "🔧 Fixing PostgreSQL user sequence..."
python manage.py fix_user_sequence

echo ""
echo "👥 Creating default production users..."
python manage.py create_production_users

echo ""
echo "🔍 Checking user status..."
python manage.py check_users

echo ""
echo "========================================="
echo "✅ Build Complete!"
echo "========================================="
