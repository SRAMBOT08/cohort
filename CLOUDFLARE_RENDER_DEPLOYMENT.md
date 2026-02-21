# Cohort Summit - Cloudflare + Render + Supabase Deployment

Complete deployment guide for the three-tier architecture:
- **Frontend**: Cloudflare Pages
- **Backend**: Render
- **Database**: Supabase PostgreSQL

---

## 🎯 Architecture Overview

```
┌─────────────────────┐
│  Cloudflare Pages   │  Frontend (React + Vite)
│  cohort-summit.pages│
└──────────┬──────────┘
           │ API Calls
           ↓
┌─────────────────────┐
│   Render Web        │  Backend (Django REST API)
│  cohort-summit      │
└──────────┬──────────┘
           │ Database
           ↓
┌─────────────────────┐
│   Supabase          │  PostgreSQL Database
│   cohort-summit-db  │
└─────────────────────┘
```

---

## Part 1: Supabase Database Setup

### Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Click **"New Project"**
3. Fill in:
   - **Name**: `cohort-summit-db`
   - **Database Password**: Generate strong password (SAVE THIS!)
   - **Region**: Choose closest to you
4. Click **"Create new project"**
5. Wait 2-3 minutes for setup

### Step 2: Get Database Connection String

1. Go to **Project Settings** → **Database**
2. Scroll to **Connection string** → **URI**
3. Copy and replace `[YOUR-PASSWORD]`:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
4. Save this securely - needed for Render

---

## Part 2: Render Backend Deployment

### Step 3: Create Render Web Service

1. Go to [https://render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:

**Service Details:**
```
Name: cohort-summit
Region: Oregon (US West)
Branch: main
Root Directory: backend
Runtime: Python 3
```

**Build Command:**
```bash
pip install --upgrade pip setuptools wheel && pip install setuptools==69.5.1 && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile -
```

### Step 4: Set Backend Environment Variables

Click **"Advanced"** → **"Environment Variables"**

#### Required Variables:

```bash
# Database (from Supabase)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres

# Django Security
SECRET_KEY=[Generate with: python3 -c "import secrets; print(secrets.token_urlsafe(50))"]
JWT_SECRET_KEY=[Generate another unique key]
DEBUG=False
ALLOWED_HOSTS=cohort-summit.onrender.com

# CORS - Will update after frontend deployment
CORS_ALLOWED_ORIGINS=http://localhost:5173
CORS_ALLOW_CREDENTIALS=True

# Static Files
STATIC_ROOT=staticfiles
STATIC_URL=/static/
```

#### Optional Email Variables:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Cohort Summit <your-email@gmail.com>
```

### Step 5: Deploy Backend

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for build
3. Check logs for success
4. Your backend URL: `https://cohort-summit.onrender.com`

### Step 6: Create Superuser

1. Go to your service → **Shell**
2. Run:
   ```bash
   cd backend
   python manage.py createsuperuser
   ```
3. Test at: `https://cohort-summit.onrender.com/admin/`

---

## Part 3: Cloudflare Pages Frontend Deployment

### Step 7: Install Wrangler CLI (Optional)

For local testing and deployment via CLI:

```bash
npm install -g wrangler
wrangler login
```

### Step 8: Deploy via Cloudflare Dashboard (Recommended)

1. Go to [https://dash.cloudflare.com](https://dash.cloudflare.com)
2. Navigate to **Workers & Pages**
3. Click **"Create application"** → **"Pages"** → **"Connect to Git"**

### Step 9: Configure Cloudflare Pages

1. **Select repository**: `cohort` (or your repo name)
2. **Project name**: `cohort-summit-frontend`

**Build Configuration:**
```
Framework preset: Vite
Build command: npm install && npm run build
Build output directory: dist
Root directory: (leave empty)
```

### Step 10: Set Frontend Environment Variables

In Cloudflare Pages → **Settings** → **Environment variables**:

```bash
# Production Variables
VITE_API_URL=https://cohort-summit.onrender.com
NODE_VERSION=18
NODE_ENV=production
```

**Important:** Remove any trailing slashes from `VITE_API_URL`!

### Step 11: Deploy Frontend

1. Click **"Save and Deploy"**
2. Wait 2-3 minutes for build
3. Your frontend URL: `https://cohort-summit-frontend.pages.dev`

### Step 12: Update Backend CORS

Now that frontend is deployed, update backend:

1. Go to Render → Your service → **Environment**
2. Update `CORS_ALLOWED_ORIGINS`:
   ```
   https://cohort-summit-frontend.pages.dev
   ```
3. If you have custom domain:
   ```
   https://cohort-summit-frontend.pages.dev,https://your-domain.com
   ```
4. Save (backend will redeploy)

---

## Part 4: Custom Domain (Optional)

### For Frontend (Cloudflare Pages)

1. Cloudflare Pages → **Custom domains**
2. Click **"Set up a custom domain"**
3. Enter: `app.yourdomain.com`
4. Follow DNS setup instructions
5. SSL is automatic ✅

### For Backend (Render)

1. Render service → **Settings** → **Custom Domain**
2. Add: `api.yourdomain.com`
3. Add CNAME record in your DNS:
   ```
   CNAME api.yourdomain.com → cohort-summit.onrender.com
   ```
4. Update `ALLOWED_HOSTS` in Render environment

---

## ✅ Post-Deployment Verification

### Backend Health Check

```bash
# Test API
curl https://cohort-summit.onrender.com/health/
# Should return: {"status": "healthy"}

# Test admin
open https://cohort-summit.onrender.com/admin/
```

### Frontend Check

1. Visit: `https://cohort-summit-frontend.pages.dev`
2. Should see Cohort Summit login page
3. Check browser console - no CORS errors
4. Test login with superuser

### Full Integration Test

1. Open frontend
2. Login with credentials
3. Navigate through all pages
4. Test API calls (check Network tab)
5. Verify all 5 pillars load

---

## 🔧 Troubleshooting

### Frontend Can't Connect to Backend

**Check:**
- `VITE_API_URL` is correct in Cloudflare env vars
- No trailing slash on API URL
- Backend CORS includes frontend URL
- Backend service is running

**Fix:**
```bash
# In Cloudflare Pages settings
VITE_API_URL=https://cohort-summit.onrender.com

# In Render backend environment
CORS_ALLOWED_ORIGINS=https://cohort-summit-frontend.pages.dev
```

### CORS Errors in Browser

**Error:** `Access to fetch at '...' has been blocked by CORS policy`

**Solution:**
1. Check backend `CORS_ALLOWED_ORIGINS` includes exact frontend URL
2. Verify `CORS_ALLOW_CREDENTIALS=True`
3. No trailing slashes in either URL
4. Frontend and backend must both use HTTPS in production

### Build Fails on Cloudflare

**Error:** `Module not found` or build errors

**Solution:**
1. Check `NODE_VERSION=18` is set
2. Verify `package.json` has all dependencies
3. Test build locally: `npm run build`
4. Check build logs for specific errors

### Backend Not Starting on Render

**Error:** `ModuleNotFoundError: No module named 'pkg_resources'`

**Solution:** Already fixed in latest code ✅
- drf-yasg is disabled
- setuptools==69.5.1 is installed first
- If still failing, clear build cache

---

## 🚀 Continuous Deployment

### Automatic Deployments

Both platforms auto-deploy on git push:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Cloudflare Pages deploys frontend (1-2 min)
# Render deploys backend (3-5 min)
```

### Preview Deployments (Cloudflare)

- Every PR gets a preview URL
- Test before merging to main
- Automatic preview links in GitHub PRs

---

## 💰 Cost Breakdown

### Free Tier
- **Cloudflare Pages**: Free (500 builds/month, unlimited bandwidth)
- **Render Web Service**: Free (spins down after 15min inactivity)
- **Supabase**: Free (500MB DB, 2GB bandwidth)
- **Total: $0/month**

### Production Tier
- **Cloudflare Pages**: $20/month (Pro - better performance)
- **Render Web Service**: $7/month (Starter - always on)
- **Supabase**: $25/month (Pro - 8GB DB)
- **Total: $52/month**

---

## 🔐 Security Checklist

- [ ] `SECRET_KEY` is unique and secure
- [ ] `JWT_SECRET_KEY` is unique and different from SECRET_KEY
- [ ] `DEBUG=False` in production
- [ ] `CORS_ALLOWED_ORIGINS` contains only your domains
- [ ] HTTPS enabled on all services (automatic)
- [ ] Database password is strong (from Supabase)
- [ ] No secrets in git repository
- [ ] Environment variables set in platform dashboards

---

## 📚 Useful Commands

### Frontend (Cloudflare)

```bash
# Deploy via CLI
wrangler pages deploy dist --project-name=cohort-summit-frontend

# View logs
wrangler pages deployment tail

# Local preview
npm run build && wrangler pages dev dist
```

### Backend (Render)

```bash
# View logs
# Go to Render Dashboard → Logs

# Run commands via Shell
# Go to Render Dashboard → Shell
cd backend
python manage.py migrate
python manage.py createsuperuser
```

### Database (Supabase)

```bash
# Connect via psql
psql "postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"

# Or use Supabase SQL Editor in dashboard
```

---

## 🎯 Quick Reference

| Service | Platform | URL |
|---------|----------|-----|
| Frontend | Cloudflare Pages | `https://cohort-summit-frontend.pages.dev` |
| Backend | Render | `https://cohort-summit.onrender.com` |
| Database | Supabase | `db.xxx.supabase.co` |
| Admin Panel | Backend | `https://cohort-summit.onrender.com/admin/` |

---

## 📖 Additional Resources

- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Render Deployment Docs](https://render.com/docs/deploy-django)
- [Supabase Database Docs](https://supabase.com/docs/guides/database)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)

---

**Last Updated:** February 21, 2026  
**Architecture:** Cloudflare + Render + Supabase  
**Status:** Production Ready ✅
