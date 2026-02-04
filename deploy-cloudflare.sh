#!/bin/bash

# Cloudflare Pages Deployment Script
# This script builds and deploys your frontend to Cloudflare Pages

set -e  # Exit on error

echo "🚀 Starting Cloudflare Pages Deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check if wrangler is installed
echo ""
echo "${YELLOW}Step 1: Checking prerequisites...${NC}"
if ! command -v wrangler &> /dev/null; then
    echo "${RED}Wrangler CLI not found. Installing...${NC}"
    npm install -g wrangler
fi
echo "${GREEN}✓ Wrangler CLI found${NC}"

# Step 2: Install dependencies
echo ""
echo "${YELLOW}Step 2: Installing dependencies...${NC}"
npm install
echo "${GREEN}✓ Dependencies installed${NC}"

# Step 3: Load environment variables
echo ""
echo "${YELLOW}Step 3: Loading environment variables...${NC}"
if [ -f .env.cloudflare ]; then
    export $(cat .env.cloudflare | grep -v '^#' | xargs)
    echo "${GREEN}✓ Environment variables loaded from .env.cloudflare${NC}"
else
    echo "${RED}Warning: .env.cloudflare not found${NC}"
fi

# Step 4: Build the project
echo ""
echo "${YELLOW}Step 4: Building project...${NC}"
npm run build
echo "${GREEN}✓ Build complete${NC}"

# Step 5: Check build output
echo ""
echo "${YELLOW}Step 5: Verifying build output...${NC}"
if [ ! -d "dist" ]; then
    echo "${RED}Error: dist directory not found${NC}"
    exit 1
fi
echo "${GREEN}✓ Build output verified${NC}"

# Step 6: Deploy to Cloudflare Pages
echo ""
echo "${YELLOW}Step 6: Deploying to Cloudflare Pages...${NC}"
wrangler pages deploy dist --project-name=cohort-web

echo ""
echo "${GREEN}========================================${NC}"
echo "${GREEN}✓ Deployment Complete!${NC}"
echo "${GREEN}========================================${NC}"
echo ""
echo "Your site is now live on Cloudflare Pages!"
echo ""
echo "Next steps:"
echo "1. Visit your Cloudflare Pages dashboard to see deployment details"
echo "2. Test your site at the provided URL"
echo "3. Set up a custom domain (optional)"
echo ""
