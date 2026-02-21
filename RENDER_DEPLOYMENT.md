# Cohort Summit - Render Deployment Guide

Complete guide for deploying Cohort Summit on Render.com

## 📋 Prerequisites

- [Render account](https://render.com) (free tier available)
- GitHub/GitLab repository with your code
- PostgreSQL database (will be created on Render)

## 🚀 Quick Deploy

### Option 1: Deploy from render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create a new Blueprint on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Select the repository with `render.yaml`
   - Render will automatically detect and deploy all services

3. **Configure Environment Variables**
   Update these in the Render dashboard after deployment:
   - `ALLOWED_HOSTS` - Add your Render domain
   - `CORS_ALLOWED_ORIGINS` - Add your frontend URL
   - `LINKEDIN_CLIENT_ID` (optional - for IIPC module)
   - `LINKEDIN_CLIENT_SECRET` (optional)
   - `EMAIL_HOST` (optional)
   - `EMAIL_HOST_USER` (optional)
   - `EMAIL_HOST_PASSWORD` (optional)

### Option 2: Manual Setup

1. **Create PostgreSQL Database**
   - New → PostgreSQL
   - Name: `cohort-summit-db`
   - Choose plan (Free/Starter)
   - Create Database

2. **Create Web Service**
   - New → Web Service
   - Connect repository
   - Name: `cohort-summit-backend`
   - Region: Choose closest to users
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command:
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate --no-input
     ```
   - Start Command:
     ```bash
     gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
     ```

3. **Configure Environment Variables** (see section below)

## 🔐 Environment Variables

### Required Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | Auto-generated | Django secret key |
| `DATABASE_URL` | From database | Auto-linked from DB |
| `JWT_SECRET_KEY` | Auto-generated | JWT signing key |
| `DEBUG` | `False` | Production mode |
| `PYTHON_VERSION` | `3.10` | Python runtime |
| `DJANGO_SETTINGS_MODULE` | `config.settings` | Settings module |

### URLs and Origins

| Variable | Example | Notes |
|----------|---------|-------|
| `ALLOWED_HOSTS` | `.onrender.com,yourdomain.com` | Comma-separated |
| `CSRF_TRUSTED_ORIGINS` | `https://cohort-summit-backend.onrender.com` | Full URLs |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend.com,http://localhost:5173` | Frontend URLs |
| `CORS_ALLOW_CREDENTIALS` | `True` | Allow cookies |

### Optional - Email Configuration

| Variable | Example | Notes |
|----------|---------|-------|
| `EMAIL_HOST` | `smtp.gmail.com` | SMTP server |
| `EMAIL_PORT` | `587` | SMTP port |
| `EMAIL_USE_TLS` | `True` | Use TLS |
| `EMAIL_HOST_USER` | `your-email@gmail.com` | SMTP username |
| `EMAIL_HOST_PASSWORD` | `your-app-password` | SMTP password |

### Optional - LinkedIn OAuth (IIPC Module)

| Variable | Example | Notes |
|----------|---------|-------|
| `LINKEDIN_CLIENT_ID` | `your-client-id` | LinkedIn app ID |
| `LINKEDIN_CLIENT_SECRET` | `your-client-secret` | LinkedIn secret |
| `LINKEDIN_REDIRECT_URI` | `https://your-app.com/callback` | OAuth callback |

## 📦 Post-Deployment Setup

### 1. Create Superuser

Access the Render shell:
```bash
# In Render Dashboard → Service → Shell
python manage.py createsuperuser
```

Or use the management command:
```bash
python manage.py shell
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'password123')
```

### 2. Initialize Database (First-Time Only)

Visit the setup endpoint (one-time use):
```
https://your-app.onrender.com/api/setup-database/
```

### 3. Verify Deployment

Check health endpoints:
- Main: `https://your-app.onrender.com/health/`
- API: `https://your-app.onrender.com/api/health/`
- Readiness: `https://your-app.onrender.com/health/ready/`
- Liveness: `https://your-app.onrender.com/health/live/`

### 4. Access Admin Panel

Navigate to:
```
https://your-app.onrender.com/admin/
```

## 🔧 Common Issues & Solutions

### Issue: Build Fails

**Solution:** Check Python version compatibility
```yaml
# In render.yaml, ensure:
envVars:
  - key: PYTHON_VERSION
    value: "3.10"
```

### Issue: Static Files Not Loading

**Solution:** Ensure collectstatic runs in build command
```bash
python manage.py collectstatic --no-input
```

Add to settings.py:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Issue: Database Connection Error

**Solution:** Verify DATABASE_URL is linked correctly
- In Render dashboard, ensure DB is linked to web service
- Check environment variable is set: `DATABASE_URL`

### Issue: CORS Errors

**Solution:** Update CORS settings
```python
# Add to environment variables:
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:5173
CORS_ALLOW_CREDENTIALS=True
```

### Issue: 502 Bad Gateway

**Solution:** Check logs and adjust worker timeout
```bash
# In start command:
gunicorn config.wsgi:application --timeout 120 --workers 4
```

## 📊 Monitoring

### Health Checks

Render automatically monitors:
- `/health/` - Main health check
- Service uptime and performance
- Database connectivity

### View Logs

Access logs in Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. View real-time application logs

### Metrics

Monitor in Render dashboard:
- Request count
- Response time
- Error rate
- Database connections

## 💾 Backups

### Database Backups

**Automatic backups** (on paid plans):
- Daily automated backups
- Point-in-time recovery
- 30-day retention

**Manual backup:**
```bash
# In Render shell
pg_dump $DATABASE_URL > backup.sql
```

### Media Files

Media files are stored on persistent disk:
- Location: `/opt/render/project/src/media`
- Size: 5GB (adjustable in render.yaml)
- Persists across deploys

## 🔄 Updates & Redeployment

### Automatic Deployment

When you push to `main` branch:
1. Render detects changes
2. Runs build command
3. Runs migrations
4. Restarts service

### Manual Deployment

In Render dashboard:
1. Go to your service
2. Click "Manual Deploy"
3. Choose branch
4. Click "Deploy"

### Rolling Back

1. Go to "Deploys" tab
2. Find previous successful deploy
3. Click "Rollback to this deploy"

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] Database created and linked
- [ ] Superuser created
- [ ] Static files collecting properly
- [ ] Health checks passing
- [ ] CORS configured correctly
- [ ] Allowed hosts set
- [ ] CSRF trusted origins set
- [ ] Email configured (optional)
- [ ] LinkedIn OAuth configured (optional)
- [ ] Persistent disk for media files
- [ ] Monitoring enabled
- [ ] Backup strategy in place

## 📱 Frontend Deployment

After backend is deployed:

1. **Update frontend .env:**
   ```env
   VITE_API_URL=https://cohort-summit-backend.onrender.com
   ```

2. **Deploy frontend** (Render Static Site):
   - New → Static Site
   - Connect repository
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

3. **Update backend CORS:**
   ```
   CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com
   ```

## 🆘 Support

### Render Documentation
- [Python Apps on Render](https://render.com/docs/deploy-django)
- [Environment Variables](https://render.com/docs/environment-variables)
- [PostgreSQL on Render](https://render.com/docs/databases)

### Render Status
- [Status Page](https://status.render.com)

### Application Logs
- View logs in Render dashboard
- Check health endpoints for service status

## 🔗 Useful Links

- **Application:** `https://cohort-summit-backend.onrender.com`
- **Admin Panel:** `https://cohort-summit-backend.onrender.com/admin/`
- **API Docs:** `https://cohort-summit-backend.onrender.com/api/docs/`
- **Health Check:** `https://cohort-summit-backend.onrender.com/health/`

---

**Last Updated:** February 2026  
**Application:** Cohort Summit v1.0
