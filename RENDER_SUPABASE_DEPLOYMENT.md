# Cohort Summit - Render + Supabase Deployment Guide

Complete step-by-step instructions for deploying Cohort Summit to Render with Supabase PostgreSQL database.

---

## 📋 Pre-Deployment Checklist

- [ ] GitHub repository is up to date with all latest changes
- [ ] All code is tested locally and working
- [ ] Environment variables documented
- [ ] Database migrations are ready

---

## Part 1: Supabase Database Setup

### Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Click **"Start your project"** or **"New Project"**
3. Sign in with GitHub (recommended) or email
4. Click **"New Project"** in your organization
5. Fill in project details:
   - **Name**: `cohort-summit` (or your preferred name)
   - **Database Password**: Generate a strong password (SAVE THIS!)
   - **Region**: Choose closest to your users (e.g., `us-east-1`, `eu-west-1`)
   - **Pricing Plan**: Free tier is fine for testing
6. Click **"Create new project"**
7. Wait 2-3 minutes for provisioning to complete

### Step 2: Get Database Connection Details

1. In your Supabase project dashboard, click **"Project Settings"** (gear icon in sidebar)
2. Go to **"Database"** section in the left menu
3. Scroll down to **"Connection string"** section
4. Copy the **"URI"** connection string (it looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
5. **IMPORTANT**: Replace `[YOUR-PASSWORD]` with your actual database password from Step 1

### Step 3: Note Down These Credentials

Create a temporary note with these values (you'll need them for Render):

```
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
```

**Alternative format** (if URI doesn't work):
```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=[YOUR-PASSWORD]
DB_HOST=db.xxx.supabase.co
DB_PORT=5432
```

---

## Part 2: Render Web Service Setup

### Step 4: Create Render Account and Service

1. Go to [https://render.com](https://render.com)
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with GitHub (recommended)
4. Authorize Render to access your GitHub repositories
5. Click **"New +"** button in top right
6. Select **"Web Service"**

### Step 5: Connect Your Repository

1. If you see your repository (`cohort/cohort`), click **"Connect"**
2. If NOT visible:
   - Click **"Configure account"** next to GitHub
   - Grant access to your repository
   - Return to Render and refresh
   - Click **"Connect"** on your repository

### Step 6: Configure Web Service Settings

Fill in the following details:

**Basic Settings:**
```
Name: cohort-summit
Region: Oregon (US West) or closest to you
Branch: main
Root Directory: backend
```

**Build Settings:**
```
Runtime: Python 3
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
Start Command: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2
```

**Instance Type:**
- Select **"Free"** (for testing) or **"Starter"** ($7/month for production)

### Step 7: Set Environment Variables

Click **"Advanced"** to expand, then scroll to **"Environment Variables"**

Add these variables one by one (click **"Add Environment Variable"** for each):

#### Required Django Settings

```
SECRET_KEY
Value: [Generate using command below]
```

To generate SECRET_KEY, run locally:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

```
JWT_SECRET_KEY
Value: [Generate using same command above]
```

```
DEBUG
Value: False
```

```
ALLOWED_HOSTS
Value: cohort-summit.onrender.com
```
*(Replace `cohort-summit` with YOUR actual Render service name)*

#### Database Configuration

```
DATABASE_URL
Value: postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
```
*(Use the connection string from Supabase Step 2)*

#### CORS Configuration

```
CORS_ALLOWED_ORIGINS
Value: https://cohort-summit-frontend.onrender.com
```
*(We'll set this up in Part 3 - you can update it later)*

For now, during testing, you can use:
```
CORS_ALLOWED_ORIGINS
Value: http://localhost:5173,http://localhost:5174
```

```
CORS_ALLOW_CREDENTIALS
Value: True
```

#### Email Configuration (Optional but Recommended)

For password reset and notifications:

```
EMAIL_BACKEND
Value: django.core.mail.backends.smtp.EmailBackend
```

```
EMAIL_HOST
Value: smtp.gmail.com
```
*(or your email provider's SMTP server)*

```
EMAIL_PORT
Value: 587
```

```
EMAIL_USE_TLS
Value: True
```

```
EMAIL_HOST_USER
Value: your-email@gmail.com
```

```
EMAIL_HOST_PASSWORD
Value: your-app-password
```
*(For Gmail, create an App Password in Google Account settings)*

```
DEFAULT_FROM_EMAIL
Value: Cohort Summit <your-email@gmail.com>
```

#### Static Files (Required)

```
STATIC_ROOT
Value: staticfiles
```

```
STATIC_URL
Value: /static/
```

### Step 8: Deploy Backend

1. Scroll to bottom and click **"Create Web Service"**
2. Render will start building your application
3. Watch the logs for any errors
4. Build takes 3-5 minutes typically
5. Once complete, you'll see **"Your service is live 🎉"**

### Step 9: Verify Backend Deployment

1. Click on your service URL (e.g., `https://cohort-summit.onrender.com`)
2. You'll likely see a Django error page or 404 - this is NORMAL
3. Test these endpoints:

```
https://cohort-summit.onrender.com/api/auth/check/
Should return: {"authenticated": false}

https://cohort-summit.onrender.com/admin/
Should show Django admin login page
```

4. If you see these, backend is working! ✅

### Step 10: Create Superuser

Your database is empty. Create an admin user:

1. In Render dashboard, go to your service
2. Click **"Shell"** in the top menu
3. Run these commands:

```bash
cd backend
python manage.py createsuperuser
```

Follow the prompts:
- Email: your-email@example.com
- Username: admin
- Password: [create a strong password]

4. Test admin login at: `https://cohort-summit.onrender.com/admin/`

---

## Part 3: Frontend Deployment to Render

### Step 11: Create Frontend Web Service

1. In Render dashboard, click **"New +"** → **"Static Site"**
2. Connect the SAME repository
3. Configure:

```
Name: cohort-summit-frontend
Branch: main
Root Directory: (leave empty)
Build Command: npm install && npm run build
Publish Directory: dist
```

4. Click **"Create Static Site"**

### Step 12: Setup Frontend Environment

1. Go to **"Environment"** tab
2. Add environment variable:

```
VITE_API_URL
Value: https://cohort-summit.onrender.com
```
*(Use your actual backend URL)*

3. Click **"Save Changes"**
4. Frontend will redeploy automatically

### Step 13: Update CORS Settings

Now that frontend is deployed:

1. Go back to **Backend** service in Render
2. Go to **"Environment"** tab
3. Find `CORS_ALLOWED_ORIGINS`
4. Update to:
```
https://cohort-summit-frontend.onrender.com
```
*(Use your actual frontend URL)*

5. Click **"Save Changes"**
6. Backend will redeploy

### Step 14: Verify Full Stack

1. Visit your frontend URL: `https://cohort-summit-frontend.onrender.com`
2. You should see the Cohort Summit login page
3. Try logging in with your superuser credentials
4. If successful, you're fully deployed! 🎉

---

## Part 4: Database Initialization (Optional)

### Step 15: Run Setup Scripts

If you need to populate initial data (campuses, floors, etc.):

1. Go to backend service → **"Shell"**
2. Run setup commands:

```bash
cd backend
python manage.py setup_database
# or specific setup scripts
python setup_floorwings.py
python setup_mentors.py
```

---

## 🔧 Troubleshooting Guide

### Issue: Build Failed - Dependencies Error

**Solution:**
1. Check `requirements.txt` has all dependencies
2. Look at build logs for specific missing package
3. Ensure Python version compatibility

### Issue: Database Connection Error

**Check:**
- `DATABASE_URL` format is correct
- Password has no special characters (or is URL-encoded)
- Supabase project is active
- Connection pooling settings in Supabase

**Fix in Supabase:**
1. Go to Project Settings → Database
2. Enable **"Connection Pooling"**
3. Use the **Transaction** mode URL instead

### Issue: Static Files Not Loading

**Solution:**
1. Verify `STATIC_ROOT=staticfiles` is set
2. Ensure build command includes `collectstatic`
3. Check `config/settings.py` has:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
```

### Issue: CORS Errors in Browser Console

**Solution:**
1. Check `CORS_ALLOWED_ORIGINS` includes frontend URL
2. Ensure no trailing slash in URLs
3. Verify `CORS_ALLOW_CREDENTIALS=True`

### Issue: 502 Bad Gateway

**Causes:**
- Application crashed during startup
- Port binding issue
- Worker timeout

**Solution:**
1. Check Render logs for errors
2. Verify start command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
3. Add `--timeout 120` to gunicorn command if needed

### Issue: Migrations Not Applied

**Solution:**
Run in Shell:
```bash
cd backend
python manage.py migrate --run-syncdb
python manage.py migrate
```

---

## 📊 Post-Deployment Checklist

- [ ] Backend URL is accessible
- [ ] Frontend URL is accessible  
- [ ] Admin panel login works
- [ ] API endpoints return correct responses
- [ ] Database connection is stable
- [ ] Static files are loading
- [ ] CORS is configured correctly
- [ ] Email sending works (if configured)
- [ ] Superuser account created
- [ ] Initial data populated
- [ ] Test user login/signup flow
- [ ] Monitor Render logs for errors

---

## 🔐 Security Recommendations

1. **Never commit `.env` file** - Already in `.gitignore` ✅
2. **Rotate SECRET_KEY** - Generate new for production
3. **Strong database password** - Use Supabase generated one
4. **Enable Supabase RLS** - Row Level Security for data protection
5. **Setup SSL** - Render provides this automatically
6. **Monitor logs** - Check Render logs regularly
7. **Backup database** - Supabase has automatic backups
8. **Rate limiting** - Consider adding Django rate limiting

---

## 💰 Cost Estimates

### Free Tier (Testing)
- Render Web Service: Free (spins down after 15min inactivity)
- Render Static Site: Free
- Supabase: Free (500MB database, 2GB bandwidth)
- **Total: $0/month**

### Production Tier
- Render Web Service: $7/month (Starter)
- Render Static Site: Free
- Supabase: $25/month (Pro plan, 8GB database)
- **Total: $32/month**

---

## 🚀 Continuous Deployment

Render automatically redeploys when you push to GitHub!

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Render will auto-deploy in 2-3 minutes
```

---

## 📚 Additional Resources

- [Render Django Docs](https://render.com/docs/deploy-django)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)

---

## 🆘 Need Help?

**Render Support:**
- Community Forum: https://community.render.com
- Support: help@render.com

**Supabase Support:**
- Discord: https://discord.supabase.com
- GitHub: https://github.com/supabase/supabase

---

**Last Updated:** February 21, 2026
**Version:** 1.0
**Project:** Cohort Summit

---

## Quick Command Reference

### Generate Secret Keys
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Local Testing Before Deploy
```bash
# Test with production settings
cd backend
export DEBUG=False
export DATABASE_URL="your-supabase-url"
python manage.py check --deploy
python manage.py collectstatic
```

### Access Render Shell
```bash
# Commands to run in Render Shell
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

**🎉 Your Cohort Summit platform is now live and ready for students!**
