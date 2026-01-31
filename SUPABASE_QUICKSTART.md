# 🚀 Supabase Quick Reference Card

## One-Line Setup

```bash
# 1. Get Supabase URL → 2. Set in .env → 3. Run migrations → 4. Deploy
export DATABASE_URL="postgresql://..." && python3 manage.py migrate && python3 manage.py createsuperuser
```

---

## 📝 Essential Commands

### Test Connection
```bash
cd backend && python3 test_supabase_connection.py
```

### Run Migrations
```bash
cd backend && python3 manage.py migrate
```

### Create Admin User
```bash
cd backend && python3 manage.py createsuperuser
```

### Full Migration (Interactive)
```bash
cd backend && ./migrate_to_supabase.sh full
```

---

## 🔗 Connection String Format

### Production (Pooled - Port 6543)
```
postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
```

### Direct (Migrations - Port 5432)
```
postgresql://postgres.[ref]:[password]@db.[ref].supabase.co:5432/postgres
```

---

## 🌍 Where to Get Connection String

1. Go to https://supabase.com → Your Project
2. **Settings** → **Database** → **Connection string**
3. Select **URI** format
4. Copy and replace `[YOUR-PASSWORD]` with actual password

---

## ⚙️ Environment Variables

### Required
```env
DATABASE_URL=postgresql://postgres.[ref]:[pass]@...
SECRET_KEY=your-django-secret-key
ALLOWED_HOSTS=.vercel.app,.railway.app,yourdomain.com
```

### Optional
```env
DEBUG=False
CORS_ALLOWED_ORIGINS=https://your-frontend.com
JWT_SECRET_KEY=your-jwt-secret
```

---

## 🚢 Platform Deployment

### Railway
```bash
railway variables set DATABASE_URL="postgresql://..."
railway up
```

### Render
1. Dashboard → Environment
2. Add `DATABASE_URL` variable
3. Deploy

### Vercel
```bash
vercel env add DATABASE_URL production
vercel --prod
```

---

## ✅ Verify Everything Works

```bash
# 1. Test connection
python3 test_supabase_connection.py

# 2. Check Django
python3 manage.py check --database default

# 3. Run server
python3 manage.py runserver

# 4. Test endpoint
curl http://localhost:8000/api/auth/token/ -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

---

## 🔧 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Connection refused | Check DATABASE_URL, verify project not paused |
| SSL required | Add `?sslmode=require` to URL or set in OPTIONS |
| Too many connections | Use port 6543 (pooled), reduce CONN_MAX_AGE |
| Password error | URL encode special characters in password |
| Migration conflict | Run `python3 manage.py migrate --fake-initial` |

---

## 📊 Table Schema Status

✅ **100% Preserved** - All tables, relationships, and constraints remain identical.

No model changes needed. Your existing Django models work as-is.

---

## 📚 Documentation

- **Full Guide**: [SUPABASE_DEPLOYMENT_GUIDE.md](SUPABASE_DEPLOYMENT_GUIDE.md)
- **Migration Summary**: [SUPABASE_MIGRATION_SUMMARY.md](SUPABASE_MIGRATION_SUMMARY.md)
- **Main README**: [README.md](README.md#database-setup)
- **Supabase Docs**: https://supabase.com/docs/guides/database

---

## 🎯 Migration Checklist

- [ ] Create Supabase project
- [ ] Get DATABASE_URL from dashboard
- [ ] Update backend/.env
- [ ] Test connection: `python3 test_supabase_connection.py`
- [ ] Run migrations: `python3 manage.py migrate`
- [ ] Create superuser: `python3 manage.py createsuperuser`
- [ ] Test locally: `python3 manage.py runserver`
- [ ] Update deployment env vars
- [ ] Deploy application
- [ ] Verify production works

---

**Made with ❤️ for seamless Supabase migration**
