#!/bin/bash

# Cohort Summit Frontend - Cloudflare Pages Deployment Script
# Uses Wrangler CLI to deploy the static site

set -e

echo "🚀 Starting Cohort Summit Frontend Deployment..."
echo ""

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI not found!"
    echo "📦 Installing wrangler globally..."
    npm install -g wrangler
fi

# Check if logged in to Cloudflare
echo "🔐 Checking Cloudflare authentication..."
if ! wrangler whoami &> /dev/null; then
    echo "🔑 Please login to Cloudflare:"
    wrangler login
fi

# Build the frontend
echo "🔨 Building frontend..."
npm install
npm run build

# Check if dist folder exists
if [ ! -d "dist" ]; then
    echo "❌ Build failed! dist/ folder not found."
    exit 1
fi

echo "✅ Build successful!"
echo ""

# Deploy to Cloudflare Pages
echo "☁️  Deploying to Cloudflare Pages..."
wrangler pages deploy dist --project-name=cohort-summit-frontend

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your site will be available at: https://cohort-summit-frontend.pages.dev"
