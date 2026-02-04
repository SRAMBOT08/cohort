# 🚀 Cloudflare Pages Quick Reference

## Deploy Commands

### Option 1: Via Cloudflare Dashboard (Recommended for First Time)
1. Go to https://dash.cloudflare.com/
2. **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
3. Select `SRAMBOT08/cohort` repository
4. Configure:
   - **Build command**: `npm run build`
   - **Build output**: `dist`
   - **Branch**: `main_deploy`
5. Add environment variables (see below)
6. Click **Save and Deploy**

### Option 2: Via Script
```bash
# One-time setup
npm install -g wrangler
wrangler login

# Deploy
./deploy-cloudflare.sh
```

### Option 3: Manual
```bash
npm install
npm run build
wrangler pages deploy dist --project-name=cohort-web
```

---

## Environment Variables (Add in Cloudflare Dashboard)

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://cohort-37ur.onrender.com/api` |
| `VITE_APP_URL` | `https://cohort.pages.dev` |
| `VITE_SUPABASE_URL` | `https://yfoopcuwdyotlukbkoej.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Copy from `.env.cloudflare` |

---

## After Deployment: Update Backend CORS

In **Render Dashboard** → **cohort-web-app** → **Environment**:

Add to `CORS_ALLOWED_ORIGINS`:
```
https://cohort.pages.dev,https://cohort-37ur.onrender.com
```

---

## Troubleshooting

**404 on page refresh?**
→ File `public/_redirects` already created ✅

**API calls fail?**
→ Update `CORS_ALLOWED_ORIGINS` in Render backend

**Build fails?**
→ Check environment variables in Cloudflare dashboard

---

## Project Structure

```
Frontend (Cloudflare Pages)  ← Static files, global CDN
    ↓ API calls
Backend (Render)             ← Django REST API
    ↓ Database queries
Supabase                     ← PostgreSQL + Auth
```

---

## Deployment URLs

After first deployment, you'll get:
- **Production**: `https://cohort-web.pages.dev`
- **Preview (PR)**: `https://[hash].cohort-web.pages.dev`

Update `VITE_APP_URL` to match your production URL!
