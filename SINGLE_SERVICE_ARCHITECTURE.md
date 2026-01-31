# Single-Service Deployment Architecture

## Overview

Your application is now configured for **single-service deployment** on Render, where both the React frontend and Django backend run on the same service.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│          cohort-app.onrender.com (Port $PORT)       │
│                                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │         Django ASGI Server (Daphne)          │ │
│  │                                              │ │
│  │  ┌────────────────┐   ┌──────────────────┐ │ │
│  │  │  React Build   │   │   Django API     │ │ │
│  │  │  (Static)      │   │   /api/*         │ │ │
│  │  │  Served by     │   │                  │ │ │
│  │  │  Django        │   │  - CLT           │ │ │
│  │  │                │   │  - SRI           │ │ │
│  │  │  Routes:       │   │  - CFC           │ │ │
│  │  │  /, /dashboard │   │  - IIPC          │ │ │
│  │  │  /login, etc   │   │  - SCD           │ │ │
│  │  └────────────────┘   │  - Gamification  │ │ │
│  │                       │  - Admin         │ │ │
│  │                       └──────────────────┘ │ │
│  └──────────────────────────────────────────────┘ │
│                          │                          │
└──────────────────────────┼──────────────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    Supabase     │
                  │   PostgreSQL    │
                  │   (External)    │
                  └─────────────────┘
```

## How It Works

### 1. Build Process
```bash
# On Render, this happens automatically:
npm install              # Install frontend dependencies
npm run build           # Build React app → dist/
cd backend
pip install -r requirements.txt
python manage.py collectstatic  # Collect static + React build
python manage.py migrate        # Run database migrations
```

### 2. Request Routing

**Django URLs (backend/config/urls.py):**
```python
# API routes (handled first)
/api/auth/token/           → JWT authentication
/api/clt/                  → CLT module
/api/dashboard/            → Dashboard data
/admin/                    → Django admin
/media/                    → User uploads

# Catch-all route (handled last)
/*                         → Serve React app (index.html)
```

### 3. Static Files

**Django serves two types of static content:**

1. **Django static files** (CSS, admin panel, etc.)
   - Location: `backend/staticfiles/`
   - URL: `/static/`

2. **React build files** (JS, CSS, assets)
   - Location: `dist/` (built from React app)
   - Included via `STATICFILES_DIRS` in settings
   - Served at root `/`

### 4. Frontend API Calls

**Environment variable:** `VITE_API_URL=/api`

React makes requests like:
```javascript
// In production:
fetch('/api/auth/token/')  // Same origin, no CORS needed!

// In development (npm run dev):
fetch('http://localhost:8000/api/auth/token/')  // Proxied by Vite
```

## File Structure

```
cohort/
├── render.yaml                 # Single service definition
├── package.json               # Frontend dependencies
├── vite.config.js            # Vite config (dev proxy)
├── dist/                     # React build output (created)
│   ├── index.html
│   ├── assets/
│   └── ...
└── backend/
    ├── manage.py
    ├── requirements.txt      # Backend dependencies
    ├── config/
    │   ├── settings.py      # Serves React build
    │   └── urls.py          # Catch-all route
    └── staticfiles/         # Django + React static
```

## Key Configuration Files

### 1. render.yaml
```yaml
services:
  - type: web
    name: cohort-app
    runtime: python
    buildCommand: |
      npm install && npm run build  # Build frontend
      cd backend
      pip install -r requirements.txt
      python manage.py collectstatic --no-input
      python manage.py migrate
    startCommand: cd backend && daphne -b 0.0.0.0 -p $PORT config.asgi:application
    envVars:
      - VITE_API_URL: /api  # Relative path!
```

### 2. backend/config/settings.py
```python
# React build directory
REACT_APP_BUILD_PATH = os.path.join(BASE_DIR.parent, 'dist')

# Include React build in static files
STATICFILES_DIRS = [
    REACT_APP_BUILD_PATH,
] if os.path.exists(REACT_APP_BUILD_PATH) else []
```

### 3. backend/config/urls.py
```python
# Catch-all route for React app (must be last!)
urlpatterns += [
    re_path(r'^(?!api/|admin/|media/|static/).*$', serve_react),
]
```

## Benefits vs Two-Service Deployment

| Aspect | Single Service | Two Services |
|--------|---------------|--------------|
| **Cost** | 1 free service | 2 services needed |
| **CORS** | Not needed (same origin) | Must configure |
| **Complexity** | Simpler setup | More moving parts |
| **URLs** | One domain | Two domains |
| **Deployment** | One config file | Two configs |
| **Maintenance** | Easier | More overhead |

## Environment Variables

### Production (Render)
```bash
# Django
SECRET_KEY=auto-generated
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=postgresql://... (Supabase)

# Frontend
VITE_API_URL=/api  # Relative path!
```

### Local Development
```bash
# Django
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Frontend (handled by Vite proxy)
VITE_API_URL=http://localhost:8000/api
```

## Request Flow Example

### Production (cohort-app.onrender.com)
```
1. User visits: https://cohort-app.onrender.com/
   → Django serves: dist/index.html

2. React loads and requests: /api/auth/token/
   → Django API handles request
   → Returns JSON response

3. User visits: https://cohort-app.onrender.com/dashboard
   → Django catch-all route serves: dist/index.html
   → React Router handles /dashboard route
```

### Development (localhost)
```
1. User visits: http://localhost:5173/
   → Vite dev server serves React

2. React requests: http://localhost:8000/api/auth/token/
   → Proxied by Vite to Django backend
   → Django API handles request

3. User visits: http://localhost:5173/dashboard
   → Vite serves React
   → React Router handles /dashboard
```

## Troubleshooting

### Frontend shows 503
**Issue:** React app not built
```
Frontend not built. Run: npm run build
```
**Solution:** Build failed during deployment. Check Render logs for npm errors.

### API calls fail with 404
**Issue:** API routes not matching
**Check:**
1. All API URLs start with `/api/`
2. Django `urls.py` has catch-all route **last**
3. React uses `VITE_API_URL=/api` in production

### Static files not loading
**Issue:** collectstatic failed
**Solution:**
```bash
# In Render shell:
cd backend
python manage.py collectstatic --no-input
```

### Can't access admin panel
**Issue:** Admin route caught by React
**Solution:** Admin route (`/admin/`) is checked **before** catch-all, should work.
If not, check `urls.py` order.

## Updating After Deployment

### Frontend changes (React)
```bash
# Push to GitHub
git add src/
git commit -m "Update frontend"
git push origin main

# Render will automatically:
# 1. npm run build
# 2. collectstatic
# 3. Restart service
```

### Backend changes (Django)
```bash
# Push to GitHub
git add backend/
git commit -m "Update backend"
git push origin main

# Render will automatically:
# 1. pip install
# 2. migrate (if needed)
# 3. Restart service
```

## Performance Considerations

### Static File Caching
- Django uses WhiteNoise for efficient static file serving
- React build files are compressed and cached
- `Cache-Control` headers set automatically

### Free Tier Limitations
- Service spins down after 15 min inactivity
- First request takes 30-60 seconds (cold start)
- Subsequent requests are fast

### Scaling Options
- Upgrade to Starter plan ($7/mo) for always-on
- Add more instances for load balancing
- Use CDN for static assets (optional)

## Security Checklist

- [x] `DEBUG=False` in production
- [x] `SECRET_KEY` auto-generated
- [x] `ALLOWED_HOSTS` restricted
- [x] Database SSL enabled (Supabase)
- [x] JWT authentication enabled
- [x] CORS not needed (same origin)
- [x] Static files served securely
- [x] HTTPS automatic (Render)

## Deployment Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] Supabase database created
- [ ] `DATABASE_URL` ready to paste
- [ ] `render.yaml` committed
- [ ] Build scripts tested locally

After deploying:
- [ ] Service shows "Live" status
- [ ] Can access frontend at `/`
- [ ] Can access API at `/api/`
- [ ] Can login to app
- [ ] Can access admin at `/admin/`

## Next Steps

1. **Custom Domain**: Add your domain in Render settings
2. **Monitoring**: Set up error tracking (Sentry, etc.)
3. **Backups**: Schedule database backups in Supabase
4. **CI/CD**: Already configured via GitHub auto-deploy
5. **Scaling**: Upgrade plan as traffic grows

---

**Architecture Type:** Monolithic Deployment
**Last Updated:** January 31, 2026
**Deployment Platform:** Render.com
**Database:** Supabase PostgreSQL
