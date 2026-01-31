# Complete Render Deployment Guide

This guide provides step-by-step instructions to deploy both frontend and backend to Render.

## 🎯 Overview

Your application will be deployed with:
- **Backend**: Django + ASGI/Daphne on `cohort-backend.onrender.com`
- **Frontend**: React + Vite (static) on `cohort-frontend.onrender.com`
- **Database**: Supabase PostgreSQL (external)

## 📋 Prerequisites

1. **GitHub Repository** - Your code must be pushed to GitHub
2. **Render Account** - Sign up at https://render.com
3. **Supabase Database** - Create a Supabase project at https://supabase.com

---

## 🚀 Step 1: Setup Supabase Database

### 1.1 Create Supabase Project
1. Go to https://supabase.com and sign in
2. Click **"New Project"**
3. Fill in:
   - **Name**: `cohort-db`
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose closest to your users
4. Wait for project to be created (~2 minutes)

### 1.2 Get Database Connection String
1. Go to **Settings** → **Database**
2. Scroll to **Connection String** section
3. Select **Connection pooling** mode
4. Copy the **URI** format connection string:
   ```
   postgresql://postgres.[ref]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with your actual password
6. **Save this connection string** - you'll need it soon!

---

## 🚀 Step 2: Deploy to Render

### 2.1 Connect Repository
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select your `cohort` repository
5. Render will detect `render.yaml` automatically

### 2.2 Configure Environment Variables

#### Before clicking "Apply", you need to set the DATABASE_URL:

1. In the Blueprint preview, find **cohort-backend** service
2. Click **"Advanced"** or look for environment variables
3. Find `DATABASE_URL` (marked as `sync: false`)
4. **Set it to your Supabase connection string**:
   ```
   postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```

#### The following will be auto-generated:
- `SECRET_KEY` - Django secret (auto-generated)
- `JWT_SECRET_KEY` - JWT signing key (auto-generated)

#### Pre-configured values:
- `PYTHON_VERSION`: 3.12.0
- `DEBUG`: False
- `ALLOWED_HOSTS`: .onrender.com,cohort-backend.onrender.com
- `CORS_ALLOWED_ORIGINS`: https://cohort-frontend.onrender.com
- `REDIS_URL`: redis://localhost:6379 (dummy for cache)

### 2.3 Deploy
1. Click **"Apply"** to start deployment
2. Render will create:
   - ✅ `cohort-backend` (Django API)
   - ✅ `cohort-frontend` (React Static Site)

### 2.4 Monitor Deployment
1. Go to **Dashboard** to see both services
2. Click on each service to view logs
3. Wait for both to show **"Live"** status (5-10 minutes)

#### Backend logs should show:
```
✅ Build complete!
Starting ASGI/Daphne server...
Daphne running on http://0.0.0.0:PORT
```

#### Frontend logs should show:
```
✅ Build complete!
Static site published to /dist
```

---

## 🚀 Step 3: Run Initial Database Migrations

Once the backend is deployed:

### 3.1 Access Render Shell
1. Go to your **cohort-backend** service in Render dashboard
2. Click **"Shell"** tab (top right)
3. This opens a terminal in your deployed app

### 3.2 Run Migrations
```bash
python manage.py migrate
```

### 3.3 Create Superuser (Optional)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 3.4 Test Admin Panel
Visit: `https://cohort-backend.onrender.com/admin/`
- Login with your superuser credentials
- Verify you can access the Django admin

---

## 🚀 Step 4: Verify Deployment

### 4.1 Test Backend API
```bash
# Test health check
curl https://cohort-backend.onrender.com/admin/login/

# Test API endpoint
curl https://cohort-backend.onrender.com/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"yourpassword"}'
```

### 4.2 Test Frontend
1. Visit: `https://cohort-frontend.onrender.com/`
2. You should see your React app
3. Try logging in with your credentials
4. Check browser console for any errors

### 4.3 Verify Database Connection
Check backend logs in Render:
- Should see: `✅ Connected to PostgreSQL`
- Should NOT see: Connection errors or timeouts

---

## 🔧 Step 5: Post-Deployment Configuration

### 5.1 Update CORS (if needed)
If your frontend URL is different, update backend environment variable:

1. Go to **cohort-backend** → **Environment**
2. Update `CORS_ALLOWED_ORIGINS`:
   ```
   https://cohort-frontend.onrender.com,https://your-custom-domain.com
   ```

### 5.2 Setup Custom Domain (Optional)
1. Go to **cohort-frontend** service
2. Click **"Settings"** → **"Custom Domain"**
3. Add your domain (e.g., `app.yourdomain.com`)
4. Follow DNS instructions provided by Render

### 5.3 Enable Auto-Deploy
Both services are configured to auto-deploy when you push to GitHub:
- Backend: Pushes to `main` branch
- Frontend: Pushes to `main` branch

---

## 📊 Service URLs

After deployment, your services will be available at:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | `https://cohort-frontend.onrender.com` | React app (user interface) |
| **Backend API** | `https://cohort-backend.onrender.com/api` | REST API endpoints |
| **Admin Panel** | `https://cohort-backend.onrender.com/admin` | Django admin interface |
| **Database** | Supabase Dashboard | Database management |

---

## 🐛 Troubleshooting

### Backend Issues

#### Build Fails
```bash
# Check logs for error
# Common issues:
- Missing dependencies in requirements.txt
- Python version mismatch
- Database connection string incorrect
```

**Solution**:
1. Verify `requirements.txt` is complete
2. Check `PYTHON_VERSION` = 3.12.0
3. Verify `DATABASE_URL` format is correct

#### Migration Errors
```
django.db.utils.OperationalError: could not connect to server
```

**Solution**:
1. Verify Supabase database is running
2. Check DATABASE_URL has correct password
3. Ensure using port **6543** (pooled connection)
4. Verify SSL mode in connection string

#### 502 Bad Gateway
```
Service Unavailable
```

**Solution**:
1. Check backend logs for crash/errors
2. Verify `startCommand` in render.yaml
3. Check if migrations ran successfully
4. Restart the service

### Frontend Issues

#### Build Fails
```
npm ERR! Failed at build script
```

**Solution**:
1. Run `npm install && npm run build` locally first
2. Fix any build errors
3. Push fixed code to GitHub
4. Redeploy on Render

#### API Calls Failing (CORS)
```
Access to fetch at 'https://cohort-backend...' has been blocked by CORS
```

**Solution**:
1. Check backend `CORS_ALLOWED_ORIGINS` includes frontend URL
2. Verify frontend `VITE_API_URL` is correct
3. Check browser console for exact error
4. Update CORS settings and redeploy backend

#### 404 on Routes
```
Cannot GET /dashboard
```

**Solution**:
- This is fixed in render.yaml with rewrite rules
- If still occurs, verify `staticPublishPath: ./dist` is correct
- Check that `routes` section exists in render.yaml

### Database Issues

#### Connection Timeout
```
psycopg.OperationalError: connection timeout
```

**Solution**:
1. Use connection pooling port **6543** (not 5432)
2. Check Supabase project is active
3. Verify connection string format:
   ```
   postgresql://postgres.[ref]:[pwd]@....pooler.supabase.com:6543/postgres
   ```

#### SSL Required Error
```
SSL connection is required
```

**Solution**:
- Already handled in `settings.py` with `sslmode=require`
- Verify you're using the pooler URL (ends with `.pooler.supabase.com`)

---

## 🔐 Security Checklist

Before going to production:

- [ ] `DEBUG = False` in backend (already set in render.yaml)
- [ ] `SECRET_KEY` is auto-generated (never hardcode)
- [ ] `JWT_SECRET_KEY` is auto-generated
- [ ] Database password is strong and secure
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] `CORS_ALLOWED_ORIGINS` only includes your frontend domain
- [ ] Supabase database has strong password
- [ ] Admin superuser has strong password
- [ ] SSL/HTTPS enabled (automatic on Render)

---

## 🎯 Quick Commands

### View Logs
```bash
# Backend logs
# Go to Render Dashboard → cohort-backend → Logs

# Frontend logs  
# Go to Render Dashboard → cohort-frontend → Logs
```

### Redeploy
```bash
# Option 1: Push to GitHub (auto-deploys)
git add .
git commit -m "Update"
git push origin main

# Option 2: Manual deploy in Render Dashboard
# Go to service → Click "Manual Deploy" → Deploy latest commit
```

### Access Shell (Backend only)
```bash
# Go to Render Dashboard → cohort-backend → Shell
# Run Django commands:
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
python manage.py collectstatic
```

### Check Service Status
```bash
# Test backend
curl https://cohort-backend.onrender.com/admin/login/

# Test frontend
curl https://cohort-frontend.onrender.com/
```

---

## 📈 Scaling & Performance

### Free Tier Limitations
- Backend spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free (enough for 1 service 24/7)

### Upgrade to Paid Plan
If you need better performance:

1. Go to service → **Settings** → **Instance Type**
2. Upgrade to **Starter** ($7/month):
   - No spin-down
   - Faster response times
   - More resources

### Database Performance
Supabase free tier includes:
- 500 MB database
- Unlimited API requests
- Auto-pauseafter 7 days inactivity

For production, consider upgrading to Pro tier.

---

## 🆘 Getting Help

### Check Logs First
1. Render Dashboard → Select service → Logs tab
2. Look for red error messages
3. Check the last few lines before failure

### Common Log Locations
- **Build logs**: Shows pip install, npm install, migrations
- **Runtime logs**: Shows server startup, requests, errors
- **Deploy logs**: Shows git pull, build process

### Contact Support
- **Render Support**: https://render.com/docs
- **Supabase Support**: https://supabase.com/docs
- **Django Docs**: https://docs.djangoproject.com

---

## ✅ Deployment Checklist

Use this checklist to ensure everything is set up correctly:

### Pre-Deployment
- [ ] Code pushed to GitHub
- [ ] Supabase project created
- [ ] Database connection string saved
- [ ] Render account created

### Deployment
- [ ] Blueprint applied in Render
- [ ] DATABASE_URL set correctly
- [ ] Both services show "Live" status
- [ ] Build logs show no errors

### Post-Deployment
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Admin panel accessible
- [ ] Frontend loads correctly
- [ ] API calls working
- [ ] Login functionality works

### Testing
- [ ] Backend health check responds
- [ ] Frontend loads in browser
- [ ] Can login and access dashboard
- [ ] All features working as expected
- [ ] No CORS errors in console
- [ ] Database queries working

---

## 🎉 Success!

Your application is now live on Render! 

- Frontend: `https://cohort-frontend.onrender.com`
- Backend: `https://cohort-backend.onrender.com`

Share the frontend URL with your users and start using your deployed application!

---

## 📝 Next Steps

1. **Monitor your application**: Check logs regularly for errors
2. **Set up monitoring**: Consider adding error tracking (Sentry)
3. **Backup database**: Regular backups via Supabase dashboard
4. **Update regularly**: Keep dependencies updated
5. **Add custom domain**: For a professional look

---

**Last Updated**: January 31, 2026
**Deployment Method**: Render Blueprint (render.yaml)
**Database**: Supabase PostgreSQL
