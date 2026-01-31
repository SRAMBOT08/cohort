# 🚀 Render Single-Service Deployment

Deploy your full-stack application (frontend + backend) to Render on ONE service in 10 minutes!

## 📦 What You'll Deploy

- ✅ Django Backend (ASGI/Daphne) + React Frontend
- ✅ Supabase PostgreSQL Database  
- ✅ Single URL for everything

**One service means:**
- ✅ Lower cost (1 service instead of 2)
- ✅ No CORS issues (same origin)
- ✅ Simpler deployment
- ✅ One domain: `cohort-app.onrender.com`

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
   - Find **cohort-app** service
   - Set `DATABASE_URL` to your Supabase connection string (from Step 1)
5. Click **"Apply"** and wait for deployment (~5-10 minutes)

### Step 3: Verify Deployment (1 minute)

Once the service shows **"Live"**:

1. Visit: `https://cohort-app.onrender.com/`
2. You should see your React app
3. Try logging in with default credentials:
   - **Admin**: username `admin`, password `admin123`
   - **Student**: username from your database

---

## ✅ Your Service URLs

Everything is on ONE domain:

| Resource | URL |
|---------|-----|
| **React App** | https://cohort-app.onrender.com/ |
| **API** | https://cohort-app.onrender.com/api/ |
| **Admin Panel** | https://cohort-app.onrender.com/admin/ |

---

## 🐛 Troubleshooting

### Service won't start?
**Check Render logs for:**
```
Error: DATABASE_URL not set
```
**Solution**: Set DATABASE_URL in environment variables

### Build fails?
```
npm ERR! or pip error
```
**Solution**: 
- Check `package.json` and `requirements.txt` are valid
- Verify Node.js 20.11.0 and Python 3.12.0 are set

### Frontend shows 503?
```
Frontend not built. Run: npm run build
```
**Solution**: Build process failed. Check logs for npm build errors.

### Can't login?
**Solution**: Create superuser via Render Shell:
```bash
python manage.py createsuperuser
```

---

## 🔧 Advanced: Custom Commands

### Access Service Shell
1. Go to **cohort-app** service → **Shell** tab
2. You're in the root directory, navigate to backend:
   ```bash
   cd backend
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py shell
   ```

### Rebuild Frontend
If you update React code:
```bash
npm run build
cd backend
python manage.py collectstatic --no-input
```
Then restart the service.

---

## 📚 Full Documentation

For detailed instructions, see [RENDER_DEPLOYMENT_COMPLETE.md](./RENDER_DEPLOYMENT_COMPLETE.md)

---

## 🎉 Done!

Your full-stack app is live on **ONE service**: `https://cohort-app.onrender.com`

**Benefits of single-service deployment:**
- ✅ Simpler than managing 2 services  
- ✅ No CORS configuration needed
- ✅ One URL for everything
- ✅ Costs less (1 free service vs 2)

**Need help?** Check logs: Render Dashboard → cohort-app → Logs
