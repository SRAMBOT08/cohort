# Render Deployment - Quick Reference

## 🚀 One-Command Deploy

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to Render Dashboard → New → Blueprint
# 3. Connect repository with render.yaml
# 4. Deploy automatically configures everything!
```

## 🔑 Essential Environment Variables to Set

After deployment, update these in Render dashboard:

```
ALLOWED_HOSTS=.onrender.com,your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend.com
```

## ✅ Health Check Endpoints

- **Main:** `/health/`
- **API:** `/api/health/`
- **Ready:** `/health/ready/`
- **Live:** `/health/live/`

## 📋 Post-Deploy Checklist

1. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

2. Visit setup endpoint (first time only):
   ```
   https://your-app.onrender.com/api/setup-database/
   ```

3. Verify health:
   ```
   https://your-app.onrender.com/health/
   ```

4. Access admin:
   ```
   https://your-app.onrender.com/admin/
   ```

## 🔄 To Redeploy

Just push to main branch:
```bash
git add .
git commit -m "Update"
git push
```

Render auto-deploys!

## 📝 Key Files

- `backend/render.yaml` - Deployment configuration
- `backend/requirements.txt` - Python dependencies
- `backend/config/settings.py` - Django settings

## 🆘 Troubleshooting

**Build fails?**
- Check Python version is 3.10
- Verify requirements.txt is complete

**Database errors?**
- Ensure DATABASE_URL is linked
- Check migrations ran successfully

**CORS errors?**
- Add frontend URL to CORS_ALLOWED_ORIGINS
- Set CORS_ALLOW_CREDENTIALS=True

**Static files missing?**
- Verify collectstatic in build command
- Check STATIC_ROOT setting

## 📚 Full Documentation

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for complete guide.
