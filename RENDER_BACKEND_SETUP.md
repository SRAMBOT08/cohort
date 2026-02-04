# Render Backend Setup Guide

## Architecture

```
┌─────────────────┐
│ Cloudflare      │  Static Frontend (HTML/JS/CSS)
│ Pages           │  Global CDN, Edge caching
└────────┬────────┘
         │ HTTPS API calls
         │
┌────────▼────────┐
│ Render          │  Django REST API
│ (Backend)       │  Port: $PORT (auto-assigned)
└────────┬────────┘
         │ Database queries + Auth
         │
┌────────▼────────┐
│ Supabase        │  PostgreSQL Database + Auth
│ (Database)      │  Connection pooling enabled
└─────────────────┘
```

## What Changed from Previous render.yaml

### ❌ Removed (Frontend moved to Cloudflare)
- Node.js installation
- `npm install` and `npm run build` steps
- Frontend build output to `backend/static/frontend`
- `NODE_VERSION` environment variable

### ✅ Kept (Backend essentials)
- Python dependencies installation
- Django static files collection
- Database migrations
- Gunicorn server
- All Supabase configuration

## Deployment Steps

### 1. Update render.yaml in Repository

The new `render.yaml` is backend-only. Commit and push:

```bash
git add render.yaml
git commit -m "chore: update render.yaml for backend-only deployment"
git push origin main_deploy
```

### 2. Deploy on Render

Render will automatically detect the push and redeploy. Or manually:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Select your service: `cohort-backend-api`
3. Click **Manual Deploy** → **Deploy latest commit**

### 3. Update CORS After Cloudflare Deployment

Once you have your Cloudflare Pages URL, update in Render Dashboard:

**Navigate to:** Environment → `CORS_ALLOWED_ORIGINS`

**Update to:**
```
https://your-app.pages.dev,http://localhost:5173
```

Replace `your-app.pages.dev` with your actual Cloudflare Pages URL.

## Environment Variables Reference

### Critical Variables to Update

| Variable | Description | Update After |
|----------|-------------|--------------|
| `CORS_ALLOWED_ORIGINS` | Allowed frontend origins | Cloudflare deployment |
| `ALLOWED_HOSTS` | Allowed backend hosts | Usually auto-set by Render |

### Pre-Configured (No changes needed)

- ✅ `SUPABASE_URL`
- ✅ `SUPABASE_JWT_SECRET`
- ✅ `SUPABASE_SERVICE_ROLE_KEY`
- ✅ `DATABASE_URL`
- ✅ JWT settings

## Health Check

Your backend exposes a health endpoint:

```bash
curl https://cohort-backend-api.onrender.com/api/health/
```

Expected response:
```json
{
  "status": "ok",
  "service": "django-supabase-auth"
}
```

## Testing the Backend

### 1. Test Health Endpoint

```bash
curl https://cohort-backend-api.onrender.com/api/health/
```

### 2. Test Authentication

```bash
curl -X POST https://cohort-backend-api.onrender.com/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test@example.com",
    "password": "password123"
  }'
```

### 3. Test Protected Endpoint

```bash
curl https://cohort-backend-api.onrender.com/api/dashboard/stats/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Connecting Frontend to Backend

In your Cloudflare Pages environment variables, set:

```bash
VITE_API_URL=https://cohort-backend-api.onrender.com/api
```

## Troubleshooting

### Issue: CORS Errors

**Symptom:** Frontend can't make API calls, browser shows CORS error

**Fix:**
1. Check `CORS_ALLOWED_ORIGINS` in Render includes your Cloudflare Pages URL
2. Ensure URL has `https://` prefix
3. No trailing slashes
4. Redeploy backend after changes

### Issue: 502 Bad Gateway

**Symptom:** Backend URL returns 502

**Cause:** Backend failed to start

**Fix:**
1. Check Render logs
2. Verify all environment variables are set
3. Check database connection string
4. Ensure `requirements.txt` is complete

### Issue: Database Connection Fails

**Symptom:** Backend logs show database errors

**Fix:**
1. Verify `DATABASE_URL` in Render
2. Check Supabase project is active
3. Verify connection pooler port: `6543`
4. Test connection from Render shell

## Performance Optimization

### 1. Enable Render Persistent Disk (Paid plan)

For media files:
```yaml
disk:
  name: media
  mountPath: /opt/render/project/src/backend/media
  sizeGB: 1
```

### 2. Increase Workers (Paid plan)

In `render.yaml`, update gunicorn:
```bash
--workers 4  # Instead of 2
```

### 3. Use Redis for Caching (Optional)

Add Redis service and update Django settings.

## Cost Breakdown

| Service | Plan | Cost |
|---------|------|------|
| Render Backend | Free | $0/month (sleeps after 15min) |
| Render Persistent Disk | N/A | Not needed for free tier |
| Supabase Database | Free | $0/month (500MB) |
| Total | | **$0/month** |

**Upgrade Options:**
- Render Starter: $7/month (no sleep, persistent disk)
- Render Standard: $25/month (better performance)

## Next Steps

1. ✅ Deploy backend on Render
2. ⬜ Deploy frontend on Cloudflare Pages
3. ⬜ Update `CORS_ALLOWED_ORIGINS` with Cloudflare URL
4. ⬜ Test full authentication flow
5. ⬜ Monitor Render logs for errors
