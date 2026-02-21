# Wrangler CLI Deployment Guide

Deploy Cohort Summit frontend to Cloudflare Pages using Wrangler CLI.

---

## Quick Start

### Option 1: Use Deployment Script (Easiest)

```bash
./deploy-frontend.sh
```

This script will:
1. Check if wrangler is installed (installs if missing)
2. Verify Cloudflare authentication
3. Build the frontend (`npm run build`)
4. Deploy to Cloudflare Pages

### Option 2: Use npm Script

```bash
npm run deploy
```

### Option 3: Manual Commands

```bash
# Install wrangler globally (one time only)
npm install -g wrangler

# Login to Cloudflare (one time only)
wrangler login

# Build and deploy
npm run build
wrangler pages deploy dist --project-name=cohort-summit-frontend
```

---

## First Time Setup

### Step 1: Install Wrangler CLI

```bash
npm install -g wrangler
```

Verify installation:
```bash
wrangler --version
```

### Step 2: Login to Cloudflare

```bash
wrangler login
```

This will:
1. Open your browser
2. Ask you to authorize wrangler
3. Save your credentials locally

### Step 3: Create Project (First Deploy Only)

On your first deployment, wrangler will ask:

```
? Create a new project? (Y/n)
```

Answer: **Y** (Yes)

Then it will create the project automatically.

---

## Deployment Commands

### Deploy to Production

```bash
# Build and deploy in one command
npm run deploy

# Or manually
npm run build
wrangler pages deploy dist --project-name=cohort-summit-frontend
```

### Deploy Specific Branch

```bash
# Deploy to production branch
npm run deploy:production

# Or manually
wrangler pages deploy dist --project-name=cohort-summit-frontend --branch=main
```

### Deploy Preview (Development)

```bash
# Deploy to preview environment
wrangler pages deploy dist --project-name=cohort-summit-frontend --branch=dev
```

---

## Environment Variables

### Set via Wrangler CLI

```bash
# Set production environment variables
wrangler pages secret put VITE_API_URL --project-name=cohort-summit-frontend
# When prompted, enter: https://cohort-summit.onrender.com

# View all secrets
wrangler pages secret list --project-name=cohort-summit-frontend
```

### Set via Dashboard (Recommended)

1. Go to: https://dash.cloudflare.com
2. **Workers & Pages** → Your project
3. **Settings** → **Environment variables**
4. Add:
   ```
   VITE_API_URL = https://cohort-summit.onrender.com
   NODE_VERSION = 18
   ```

---

## Project Configuration

The `wrangler.toml` file contains your project settings:

```toml
name = "cohort-summit-frontend"
compatibility_date = "2024-01-01"
pages_build_output_dir = "dist"
```

**Note:** For Pages deployments, most configuration is minimal. The build happens locally before deploying.

---

## Common Commands

### View Deployments

```bash
# List all deployments
wrangler pages deployment list --project-name=cohort-summit-frontend

# View specific deployment details
wrangler pages deployment tail
```

### View Logs

```bash
# Tail deployment logs
wrangler pages deployment tail --project-name=cohort-summit-frontend
```

### Rollback Deployment

Use the Cloudflare Dashboard for rollbacks:
1. Go to your project → **Deployments**
2. Find the deployment you want to restore
3. Click **...** → **Rollback to this deployment**

### Delete Project

```bash
wrangler pages project delete cohort-summit-frontend
```

---

## Troubleshooting

### Error: "Not logged in"

```bash
wrangler login
```

### Error: "Project not found"

Create the project first:
```bash
wrangler pages project create cohort-summit-frontend
```

### Error: "Build failed"

Check your build locally:
```bash
npm run build
# Should create dist/ folder
ls -la dist/
```

### Error: "VITE_API_URL not found"

Set environment variables in Cloudflare Dashboard, not in `.env` file.

Frontend `.env` files are NOT used in production - only at build time.

---

## Local Preview

Test your production build locally:

```bash
# Build for production
npm run build

# Preview locally
npm run preview

# Or use wrangler
wrangler pages dev dist
```

---

## Continuous Deployment

### Auto-deploy on Git Push

To enable automatic deployments:

1. Go to Cloudflare Dashboard
2. **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**
3. Connect your GitHub repository
4. Every push to `main` will auto-deploy

You can use BOTH:
- **Git push**: Auto-deploys from GitHub
- **Wrangler CLI**: Manual deploys from your machine

---

## Deployment Workflow

### Development Workflow

```bash
# Work on features locally
npm run dev

# Test production build locally
npm run build
npm run preview

# Deploy to preview
wrangler pages deploy dist --project-name=cohort-summit-frontend --branch=dev

# When ready, deploy to production
npm run deploy:production
```

### Production Workflow

```bash
# 1. Make changes
git add .
git commit -m "Add new feature"

# 2. Build and test locally
npm run build
npm run preview

# 3. Deploy via CLI
npm run deploy

# 4. Push to GitHub (optional - for backup)
git push origin main
```

---

## Comparison: CLI vs Dashboard

| Feature | CLI (Wrangler) | Dashboard (Git) |
|---------|----------------|-----------------|
| Deployment | Manual command | Auto on git push |
| Speed | Instant | 1-2 minutes |
| Control | Full control | Automatic |
| Previews | Yes (per branch) | Yes (per branch) |
| Rollback | Via dashboard | Via dashboard |
| Best for | Quick deployments | CI/CD pipeline |

**Recommendation:** Use CLI for quick testing, Dashboard for production automation.

---

## Project URLs

After deployment, your site will be available at:

- **Production**: `https://cohort-summit-frontend.pages.dev`
- **Preview**: `https://[commit-hash].cohort-summit-frontend.pages.dev`
- **Custom domain**: Configure in Cloudflare Dashboard

---

## Additional Resources

- [Wrangler CLI Docs](https://developers.cloudflare.com/workers/wrangler/)
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

---

**Last Updated:** February 21, 2026  
**Deployment Method:** Wrangler CLI  
**Status:** Ready to Deploy 🚀
