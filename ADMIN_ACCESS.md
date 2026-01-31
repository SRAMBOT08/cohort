# 🔐 Django Admin Access

## ✅ Server Running

**Backend ASGI Server**: http://0.0.0.0:8000
**Django Admin Panel**: http://localhost:8000/admin/

---

## 👤 Login Credentials

```
Username: admin
Password: admin123
```

---

## 📍 Available URLs

### Django Admin
- **Admin Panel**: http://localhost:8000/admin/
  - Manage users, permissions, database records
  - View all app models

### API Endpoints
- **API Root**: http://localhost:8000/api/
- **Swagger Docs**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

### WebSocket Endpoints (when Redis is running)
- **Dashboard**: `ws://localhost:8000/ws/dashboard/?token=YOUR_JWT`
- **Notifications**: `ws://localhost:8000/ws/notifications/?token=YOUR_JWT`
- **Leaderboard**: `ws://localhost:8000/ws/leaderboard/?token=YOUR_JWT`
- **Mentor**: `ws://localhost:8000/ws/mentor/{id}/?token=YOUR_JWT`
- **Student**: `ws://localhost:8000/ws/student/{id}/?token=YOUR_JWT`

---

## 🚀 Quick Commands

### Start Backend (ASGI)
```bash
cd backend
python3 -m uvicorn config.asgi:application --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
npm run dev
# Runs on http://localhost:5173
```

### Create Another Admin User
```bash
cd backend
python3 manage.py createsuperuser
```

### Run Migrations
```bash
cd backend
python3 manage.py migrate
```

### Test WebSocket Setup (requires Redis)
```bash
cd backend
python3 manage.py test_websocket
```

---

## 🔧 Development Workflow

1. **Backend** is running on port 8000 (ASGI)
2. **Frontend** run on port 5173 (Vite)
3. **Admin Panel** accessible at /admin/
4. **API** accessible at /api/

---

## 📊 What You Can Do in Admin Panel

- ✅ View and edit users
- ✅ Manage student profiles
- ✅ View submissions (CLT, CFC, IIPC, SCD)
- ✅ Manage gamification points
- ✅ View leaderboard data
- ✅ Manage announcements
- ✅ View notifications
- ✅ Manage mentor assignments

---

## 🎯 Next Steps

1. **Access Admin**: http://localhost:8000/admin/
2. **Create test users** in the admin panel
3. **Test API endpoints**: http://localhost:8000/api/
4. **Optional**: Install Redis for WebSocket features

---

**Everything is ready to use!** 🎉
