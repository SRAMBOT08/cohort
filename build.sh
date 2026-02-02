#!/bin/bash
# Build script for Render deployment
# This script prepares the application for production deployment

set -e  # Exit on error

echo "======================================"
echo "Starting Render Build Process"
echo "======================================"

# 1. Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# 2. Install Supabase Python client
echo "🔌 Installing Supabase client..."
pip install supabase

# 3. Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# 4. Build frontend
echo "🏗️  Building React frontend..."
npm run build

# 5. Frontend is already built directly into backend/static/frontend
echo "✅ Frontend built to backend/static/frontend"
echo "🔍 Checking if frontend files exist..."
ls -la backend/static/ || echo "❌ backend/static/ not found"
ls -la backend/static/frontend/ || echo "❌ backend/static/frontend/ not found"
echo "📂 Contents of backend/static/frontend:"
ls -la backend/static/frontend/assets/ || echo "❌ No assets folder"

# 6. Collect Django static files
echo "📦 Collecting Django static files..."
cd backend
echo "🔍 Current directory: $(pwd)"
echo "🔍 STATICFILES_DIRS should include: $(pwd)/static"
ls -la static/ || echo "❌ static/ not found in $(pwd)"
ls -la static/frontend/ || echo "❌ static/frontend/ not found"
python manage.py collectstatic --noinput
echo "📂 After collectstatic, staticfiles contains:"
ls -la staticfiles/ || echo "❌ staticfiles/ not found"
ls -la staticfiles/frontend/ || echo "❌ staticfiles/frontend/ not found"

# 7. Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# 8. Create cache tables (if using database cache)
echo "💾 Creating cache tables..."
python manage.py createcachetable || true

# 9. Health check
echo "✅ Build completed successfully!"
echo "======================================"
echo "Ready for deployment"
echo "======================================"

cd ..
