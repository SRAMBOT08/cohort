# 🚀 Render Deployment Quick Start

Deploy your full-stack application to Render in 10 minutes!

## 📦 What You'll Deploy

- ✅ Django Backend (ASGI/Daphne)
- ✅ React Frontend (Static)
- ✅ Supabase PostgreSQL Database

---

## ⚡ 3-Step Deployment

### Step 1: Setup Supabase (2 minutes)

1. Go to https://supabase.com → **New Project**
2. Name: `cohort-db`, Set password, Choose region
3. Wait for creation, then go to **Settings** → **Database**
4. Copy **Connection Pooling** URI:
   ```
   postgresql://postgres.[ref]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
5. Replace `[PASSWORD]` with your actual password

### Step 2: Deploy on Render (5 minutes)

1. Go to https://dashboard.render.com
2. Click **New +** → **Blueprint**
3. Connect GitHub and select `cohort` repository
4. **IMPORTANT**: Before clicking Apply, set `DATABASE_URL`:
   - Find **cohort-backend** service
   - Set `DATABASE_URL` to your Supabase connection string (from Step 1)
5. Click **"Apply"** and wait for deployment (~5-10 minutes)

### Step 3: Initialize Database (3 minutes)

Once backend is live:

1. Go to **cohort-backend** service → **Shell** tab
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```

---

## ✅ Verify Deployment

### Test Backend
```bash
curl https://cohort-backend.onrender.com/admin/login/
```

### Test Frontend
Open in browser: `https://cohort-frontend.onrender.com/`

---

## 🎯 Your URLs

| Service | URL |
|---------|-----|
| **App** | https://cohort-frontend.onrender.com |
| **API** | https://cohort-backend.onrender.com/api |
| **Admin** | https://cohort-backend.onrender.com/admin |

---

## 🐛 Troubleshooting

### Backend won't start?
- Check DATABASE_URL is set correctly
- Verify Supabase password is correct
- Ensure using port **6543** (not 5432)

### Frontend shows white page?
- Check browser console for errors
- Verify VITE_API_URL points to backend
- Check backend is running (visit `/admin/`)

### CORS errors?
- Verify `CORS_ALLOWED_ORIGINS` includes frontend URL
- Should be: `https://cohort-frontend.onrender.com`

---

## 📚 Full Documentation

For detailed instructions, see [RENDER_DEPLOYMENT_COMPLETE.md](./RENDER_DEPLOYMENT_COMPLETE.md)

---

## 🎉 Done!

Your app is live! Share the frontend URL and start using your deployed application.

**Need help?** Check the logs in Render Dashboard → Select service → Logs
