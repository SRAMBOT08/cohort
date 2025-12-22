# Deployment Guide: Backend (Render) + Frontend (GitLab Pages)

## Overview

This guide explains how to deploy:
- **Backend**: Django API on **Render**
- **Frontend**: React/Vite app on **GitLab Pages**

---

## Part 1: Deploy Backend to Render

### Step 1: Push Code to GitHub/GitLab

Make sure your code is pushed to a Git repository (GitHub or GitLab).

### Step 2: Create Render Account

1. Go to [render.com](https://render.com) and sign up
2. Connect your GitHub/GitLab account

### Step 3: Deploy via Blueprint (Recommended)

1. Click **New** → **Blueprint**
2. Select your repository containing `render.yaml`
3. Render will automatically detect the configuration
4. Click **Apply** to create:
   - Web Service (cohort-backend)
   - PostgreSQL Database (cohort-db)

### Step 4: Or Deploy Manually

1. **Create PostgreSQL Database:**
   - Click **New** → **PostgreSQL**
   - Name: `cohort-db`
   - Plan: Free
   - Click **Create Database**
   - Copy the **Internal Database URL**

2. **Create Web Service:**
   - Click **New** → **Web Service**
   - Connect your repository
   - Configure:
     - **Name**: `cohort-backend`
     - **Root Directory**: `backend`
     - **Environment**: Python 3
     - **Build Command**: `chmod +x build.sh && ./build.sh`
     - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

3. **Add Environment Variables:**
   ```
   PYTHON_VERSION=3.11.0
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   DATABASE_URL=<paste Internal Database URL>
   CORS_ALLOWED_ORIGINS=https://<your-gitlab-username>.gitlab.io
   ```

### Step 5: Deploy

Click **Create Web Service** and wait for deployment (~5-10 minutes on free tier).

### Step 6: Verify Backend

- Visit: `https://cohort-backend.onrender.com/api/health/`
- Should return: `{"status": "healthy", "message": "Cohort Backend is running"}`

### Step 7: Create Superuser (Optional)

Go to Render Dashboard → Shell and run:
```bash
python manage.py createsuperuser
```

---

## Part 2: Deploy Frontend to GitLab Pages

### Step 1: Create GitLab Repository

1. Go to [gitlab.com](https://gitlab.com) and create a new project
2. Name it (e.g., `cohort-frontend`)

### Step 2: Push Frontend Code

```bash
# Add GitLab remote
git remote add gitlab https://gitlab.com/<username>/cohort-frontend.git

# Push to GitLab
git push gitlab main
```

Or push the entire repo if it's a monorepo.

### Step 3: Update Environment Variables

Edit `.env.production` in the root:
```env
VITE_API_URL=https://cohort-backend.onrender.com/api
```

**Or** set it in `.gitlab-ci.yml`:
```yaml
variables:
  VITE_API_URL: "https://cohort-backend.onrender.com/api"
```

### Step 4: GitLab CI/CD Pipeline

The `.gitlab-ci.yml` file is already created. It will:
1. Install dependencies (`npm ci`)
2. Build the app (`npm run build`)
3. Deploy to GitLab Pages

### Step 5: Enable GitLab Pages

1. Go to **Settings** → **Pages**
2. Pages will be available at: `https://<username>.gitlab.io/<project-name>/`

### Step 6: Wait for Pipeline

1. Go to **CI/CD** → **Pipelines**
2. Wait for the pipeline to complete (green checkmark)
3. Your site will be live!

---

## Part 3: Connect Frontend to Backend

### Update CORS on Render

1. Go to Render Dashboard
2. Select your web service
3. Go to **Environment**
4. Update `CORS_ALLOWED_ORIGINS`:
   ```
   https://<username>.gitlab.io,https://<username>.gitlab.io/<project-name>
   ```
5. Click **Save Changes** (triggers redeploy)

---

## Troubleshooting

### Backend Issues

**Build fails:**
- Check `requirements.txt` for missing packages
- Ensure `build.sh` is executable

**Database connection error:**
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL database status in Render

**CORS errors:**
- Update `CORS_ALLOWED_ORIGINS` with your GitLab Pages URL

### Frontend Issues

**Pipeline fails:**
- Check Node.js version compatibility
- Run `npm ci` locally to verify dependencies

**API calls fail:**
- Verify `VITE_API_URL` is correct
- Check browser console for CORS errors
- Ensure backend is running

**404 on page refresh:**
- The `_redirects` file is created in `.gitlab-ci.yml`
- If issues persist, check GitLab Pages configuration

---

## Environment Variables Summary

### Backend (Render)

| Variable | Value |
|----------|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DEBUG` | `False` |
| `SECRET_KEY` | Auto-generated |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `DATABASE_URL` | From PostgreSQL |
| `CORS_ALLOWED_ORIGINS` | Your GitLab Pages URL |
| `JWT_SECRET_KEY` | Auto-generated |

### Frontend (GitLab)

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://cohort-backend.onrender.com/api` |

---

## Quick Reference URLs

After deployment:

- **Backend API**: `https://cohort-backend.onrender.com/api/`
- **Backend Health**: `https://cohort-backend.onrender.com/api/health/`
- **API Docs**: `https://cohort-backend.onrender.com/api/docs/`
- **Admin Panel**: `https://cohort-backend.onrender.com/admin/`
- **Frontend**: `https://<username>.gitlab.io/<project-name>/`

---

## Notes

- **Free tier limitations**: Render free tier spins down after 15 minutes of inactivity. First request may take ~30 seconds.
- **GitLab Pages**: Free for public repositories. Private repos require a GitLab subscription.
- **Media files**: For production, consider using external storage (AWS S3, Cloudinary) for user uploads.
