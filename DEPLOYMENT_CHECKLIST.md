# 🚀 Deployment Checklist - Cohort Summit (Render + Supabase)

**Complete step-by-step deployment guide for Render with Supabase PostgreSQL database.**

📖 **Full Guide:** See [RENDER_SUPABASE_DEPLOYMENT.md](RENDER_SUPABASE_DEPLOYMENT.md) for detailed instructions.

---

## ✅ Already Configured (Ready for Deployment)

- [x] **CORS Security Fixed** - Environment-based CORS configuration
- [x] **Settings Configured** - Production-ready with environment variables
- [x] **Static Files Handler** - WhiteNoise configured
- [x] **Database Support** - PostgreSQL ready (Supabase)
- [x] **JWT Authentication** - Secure token-based auth
- [x] **Cleanup Complete** - Project organized and production-ready
- [x] **Frontend index.html** - Fixed and ready in root directory

---

## 🗂️ Pre-Deployment Preparation

### Step 1: Accounts Setup

- [ ] **Supabase Account** - Create at [supabase.com](https://supabase.com)
- [ ] **Render Account** - Create at [render.com](https://render.com)
- [ ] **GitHub Repository** - Ensure all code is pushed to GitHub

### Step 2: Supabase Database Setup

- [ ] Create new Supabase project
- [ ] Save database password securely
- [ ] Copy DATABASE_URL connection string
- [ ] Verify database is active

**Example DATABASE_URL:**
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
```

### Step 3: Generate Secret Keys

Generate these locally and save them securely:

```bash
# SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(50))"

# JWT_SECRET_KEY  
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## 🔧 Render Backend Deployment

### Step 4: Create Backend Web Service

- [ ] Go to Render Dashboard → New → Web Service
- [ ] Connect your GitHub repository
- [ ] Configure service:
  - **Name:** `cohort-summit` (or your choice)
  - **Region:** Oregon (US West) or nearest
  - **Branch:** `main`
  - **Root Directory:** `backend`
  - **Runtime:** Python 3
  - **Build Command:** 
    ```bash
    pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
    ```
  - **Start Command:**
    ```bash
    gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2
    ```

### Step 5: Set Backend Environment Variables

Add these in Render Dashboard → Environment:

#### Required Variables

```bash
# Database (FROM SUPABASE)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres

# Django Security
SECRET_KEY=[YOUR-GENERATED-SECRET]
JWT_SECRET_KEY=[YOUR-GENERATED-JWT-SECRET]
DEBUG=False
ALLOWED_HOSTS=cohort-summit.onrender.com

# CORS (temporarily use localhost, update after frontend deployed)
CORS_ALLOWED_ORIGINS=http://localhost:5173
CORS_ALLOW_CREDENTIALS=True

# Static Files
STATIC_ROOT=staticfiles
STATIC_URL=/static/
```

#### Optional Email Variables

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Cohort Summit <your-email@gmail.com>
```

### Step 6: Deploy Backend

- [ ] Click "Create Web Service"
- [ ] Wait 3-5 minutes for build to complete
- [ ] Check logs for any errors
- [ ] Verify deployment success (green checkmark)

### Step 7: Create Superuser

- [ ] Go to your service → Shell tab
- [ ] Run these commands:
  ```bash
  cd backend
  python manage.py createsuperuser
  ```
- [ ] Enter email, username, and password
- [ ] Test login at: `https://cohort-summit.onrender.com/admin/`

---

## 🎨 Render Frontend Deployment

### Step 8: Create Frontend Static Site

- [ ] Render Dashboard → New → Static Site
- [ ] Connect SAME repository
- [ ] Configure:
  - **Name:** `cohort-summit-frontend`
  - **Branch:** `main`
  - **Root Directory:** (leave empty)
  - **Build Command:** `npm install && npm run build`
  - **Publish Directory:** `dist`

### Step 9: Set Frontend Environment Variable

- [ ] Add environment variable:
  ```bash
  VITE_API_URL=https://cohort-summit.onrender.com
  ```
  *(Replace with YOUR actual backend URL)*

### Step 10: Update CORS for Production

- [ ] Go back to **Backend** service
- [ ] Update `CORS_ALLOWED_ORIGINS` to your frontend URL:
  ```bash
  CORS_ALLOWED_ORIGINS=https://cohort-summit-frontend.onrender.com
  ```
- [ ] Save (backend will redeploy automatically)

---

## ✅ Post-Deployment Verification

### Step 11: Test Backend

- [ ] Visit: `https://[your-backend].onrender.com/admin/`
  - Should show Django admin login
- [ ] Visit: `https://[your-backend].onrender.com/api/auth/check/`
  - Should return: `{"authenticated": false}`
- [ ] Login to admin panel with superuser credentials
  - Verify all models are visible

### Step 12: Test Frontend

- [ ] Visit: `https://[your-frontend].onrender.com`
  - Should show Cohort Summit login page
  - Logo should load correctly
  - No CORS errors in browser console
- [ ] Test login with superuser credentials
- [ ] Verify navigation works
- [ ] Check all 5 pillars load correctly

### Step 13: Test Full Authentication Flow

- [ ] Login as admin → access admin dashboard
- [ ] Create test student account
- [ ] Login as student → verify student dashboard
- [ ] Test file uploads (if applicable)
- [ ] Test API calls from frontend

---

## 🛡️ Security Final Checks

- [ ] `SECRET_KEY` is unique (not default from settings.py)
- [ ] `JWT_SECRET_KEY` is unique and different from SECRET_KEY
- [ ] `DEBUG=False` in production environment
- [ ] `CORS_ALLOWED_ORIGINS` contains only your frontend URL
- [ ] `ALLOWED_HOSTS` contains your Render domain
- [ ] No passwords or secrets in git repository
- [ ] Supabase database password is strong
- [ ] SSL/HTTPS is enabled (automatic on Render)

---

## 📊 Monitoring & Maintenance

### Daily Monitoring (First Week)

- [ ] Check Render logs for errors
- [ ] Monitor Supabase database connections
- [ ] Verify uptime (should be 99%+)
- [ ] Check response times (<500ms)

### Database Backups

- [ ] Verify Supabase automatic backups are enabled
- [ ] Note: Supabase Pro has point-in-time recovery
- [ ] Free tier has daily backups (1-7 days retention)

### Performance Optimization

- [ ] If slow, consider upgrading Render instance
- [ ] Monitor database query performance in Supabase
- [ ] Check static file loading times
- [ ] Consider CDN for static assets (future)


---

## 🆘 Troubleshooting Common Issues

### Backend Build Fails

**Error:** `Module not found` or dependency errors
- Check `requirements.txt` has all packages
- Verify Python version compatibility
- Check build logs for specific error

### Database Connection Error

**Error:** `could not connect to server` or `authentication failed`
- Verify `DATABASE_URL` is correct
- Check Supabase database is running
- Ensure password is URL-encoded (no special chars)
- Try connection pooling URL from Supabase

### Static Files Not Loading

**Error:** Admin panel has no CSS
- Verify `STATIC_ROOT=staticfiles` is set
- Check build command includes `collectstatic`
- Confirm WhiteNoise in MIDDLEWARE in settings.py

### CORS Errors in Browser

**Error:** `blocked by CORS policy`
- Add frontend URL to `CORS_ALLOWED_ORIGINS`
- Remove trailing slashes
- Verify `CORS_ALLOW_CREDENTIALS=True`
- Check frontend URL is HTTPS

### 502 Bad Gateway

**Error:** Service unavailable
- Check Render logs for application errors
- Verify gunicorn start command is correct
- Check PORT variable binding
- Increase timeout if migrations are slow

---

## 💰 Cost Summary

### Free Tier (Testing/Personal)
- **Render Web Service:** Free (sleeps after 15min inactivity)
- **Render Static Site:** Free
- **Supabase Database:** Free (500MB, 2GB bandwidth)
- **Total:** $0/month

### Production Tier (Recommended)
- **Render Web Service:** $7/month (Starter - always on)
- **Render Static Site:** Free
- **Supabase Pro:** $25/month (8GB DB, better performance)
- **Total:** $32/month

---

## 📚 Additional Resources

- **Full Deployment Guide:** [RENDER_SUPABASE_DEPLOYMENT.md](RENDER_SUPABASE_DEPLOYMENT.md)
- **Render Docs:** https://render.com/docs/deploy-django
- **Supabase Docs:** https://supabase.com/docs
- **Django Production Checklist:** https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

---

## 🎯 Quick Command Reference

### Generate Secret Keys
```bash
python3 -c "import secrets; print('SECRET_KEY:', secrets.token_urlsafe(50))"
python3 -c "import secrets; print('JWT_SECRET_KEY:', secrets.token_urlsafe(50))"
```

### Render Shell Commands
```bash
# Navigate to backend
cd backend

# Create superuser
python manage.py createsuperuser

# Run migrations manually
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Check deployment config
python manage.py check --deploy
```

### Test Locally with Production Settings
```bash
# In backend directory
export DEBUG=False
export DATABASE_URL="your-supabase-url"
python manage.py check --deploy
python manage.py runserver
```

---

## ✨ Deployment Status

### Current Status
- ✅ Code is production-ready
- ✅ Settings configured for Supabase
- ✅ Frontend fixed (index.html in root)
- ✅ All dependencies listed
- ✅ Security settings configured

### Next Action
1. **Create Supabase project** (Part 1 of guide)
2. **Deploy backend to Render** (Part 2 of guide)  
3. **Deploy frontend to Render** (Part 3 of guide)
4. **Test everything** (verification steps above)

---

**🚀 Ready to deploy!** Open [RENDER_SUPABASE_DEPLOYMENT.md](RENDER_SUPABASE_DEPLOYMENT.md) and start with Part 1.

**Last Updated:** February 21, 2026

