# Full Stack Configuration Summary

## 🎯 Your Complete Architecture

```
┌──────────────────────────────────────┐
│  Cloudflare Pages                    │
│  https://cohort-frontend.pages.dev   │  ← FRONTEND
│  - React/Vite app                    │
│  - Static files on CDN               │
└──────────────┬───────────────────────┘
               │ API Calls (HTTPS)
               │ Authorization: Bearer <token>
┌──────────────▼───────────────────────┐
│  Render                              │
│  https://cohort-backend-api...       │  ← BACKEND
│  - Django REST API                   │
│  - Port: 10000 (auto-assigned)       │
└──────────────┬───────────────────────┘
               │ PostgreSQL + Auth
┌──────────────▼───────────────────────┐
│  Supabase                            │
│  https://yfoopcuwdyotlukbkoej...     │  ← DATABASE
│  - PostgreSQL database               │
│  - JWT authentication                │
└──────────────────────────────────────┘
```

---

## ✅ What's Configured

### Frontend (Cloudflare Pages)
- **URL**: https://cohort-frontend.pages.dev
- **Environment Variables Needed**:
  ```bash
  VITE_API_URL=https://cohort-backend-api.onrender.com/api
  VITE_SUPABASE_URL=https://yfoopcuwdyotlukbkoej.supabase.co
  VITE_SUPABASE_ANON_KEY=eyJhbGc...
  ```

### Backend (Render)
- **URL**: https://cohort-backend-api.onrender.com
- **CORS**: ✅ Configured for `https://cohort-frontend.pages.dev`
- **Database**: ✅ Connected to Supabase
- **Auth**: ✅ Supabase JWT validation enabled

### Database (Supabase)
- **URL**: https://yfoopcuwdyotlukbkoej.supabase.co
- **Connection**: ✅ Via pooler (port 6543)
- **Users Mapped**: 52 ✅

---

## 🚀 Deployment Commands

### 1. Deploy Backend (Already Done)
```bash
git add render.yaml backend/config/urls.py
git commit -m "feat: configure for Cloudflare frontend"
git push origin cloud_deploy
```

### 2. Check Cloudflare Pages Environment
In Cloudflare Dashboard → Your Pages Project → Settings → Environment Variables:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://cohort-backend-api.onrender.com/api` |
| `VITE_SUPABASE_URL` | `https://yfoopcuwdyotlukbkoej.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Your anon key |

---

## 🧪 Testing the Full Stack

### Test 1: Frontend Loads
```bash
open https://cohort-frontend.pages.dev/login
```
✅ Should show login page

### Test 2: Backend API Accessible
```bash
curl https://cohort-backend-api.onrender.com/api/health/
```
✅ Should return `{"status":"healthy"}`

### Test 3: CORS Working
Open browser console at `https://cohort-frontend.pages.dev` and run:
```javascript
fetch('https://cohort-backend-api.onrender.com/api/health/')
  .then(r => r.json())
  .then(console.log)
```
✅ Should NOT show CORS error

### Test 4: Full Login Flow
1. Go to https://cohort-frontend.pages.dev/login
2. Login with: `jabbastin.k.csd.2024@snsce.ac.in` / `pass123#`
3. Should redirect to dashboard
4. Check Network tab - API calls should succeed

---

## 🔧 If Something Doesn't Work

### CORS Errors?
**Symptom**: Browser console shows `Access to fetch blocked by CORS`

**Fix**: Verify in Render Dashboard:
1. Go to your service → Environment
2. Check `CORS_ALLOWED_ORIGINS` includes: `https://cohort-frontend.pages.dev`
3. Redeploy if changed

### API Calls Fail (404)?
**Symptom**: Frontend shows "Failed to load data"

**Fix**: Check Cloudflare environment variable:
- `VITE_API_URL` should be: `https://cohort-backend-api.onrender.com/api`
- Redeploy Cloudflare Pages after changing

### Login Fails (401)?
**Symptom**: Token errors or "Invalid credentials"

**Fix**: 
1. Check SupabaseAuthMiddleware is enabled in settings.py ✅
2. Verify SUPABASE_JWT_SECRET in Render ✅
3. Check user exists in Supabase

---

## 📋 Quick Reference

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | https://cohort-frontend.pages.dev | User interface |
| Backend API | https://cohort-backend-api.onrender.com/api | REST endpoints |
| API Docs | https://cohort-backend-api.onrender.com/api/docs/simple/ | Documentation |
| Health Check | https://cohort-backend-api.onrender.com/api/health/ | Status |
| Database | Supabase (internal) | PostgreSQL + Auth |

---

## ✅ Configuration Complete!

Your full stack is now configured:
- ✅ Frontend on Cloudflare (fast CDN)
- ✅ Backend on Render (API only)
- ✅ Database on Supabase
- ✅ CORS configured
- ✅ Authentication enabled
