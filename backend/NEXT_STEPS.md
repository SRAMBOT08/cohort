# Setup Instructions - Next Steps

## ✅ Completed
- Django converted from WSGI to ASGI
- WebSocket consumers created
- All dependencies installed:
  - channels==4.0.0
  - channels-redis==4.1.0  
  - daphne==4.2.1
  - uvicorn==0.27.0

## ⚠️ Redis Required for WebSockets

Redis is needed for WebSocket functionality. Choose ONE option:

### Option 1: Install Homebrew + Redis (Recommended)
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Redis
brew install redis

# Start Redis
brew services start redis

# Test Redis
redis-cli ping
# Should return: PONG
```

### Option 2: Use Docker
```bash
# Install Docker Desktop from: https://www.docker.com/products/docker-desktop

# Run Redis
docker run -d -p 6379:6379 --name redis-cohort redis:alpine

# Test Redis
docker exec -it redis-cohort redis-cli ping
# Should return: PONG
```

### Option 3: Use Cloud Redis (Production)
- Railway: Add Redis plugin (free tier available)
- Render: Add Redis service
- Heroku: `heroku addons:create heroku-redis:hobby-dev`
- AWS ElastiCache
- Azure Cache for Redis

## 🚀 Running the Server

### Without Redis (HTTP only - no WebSocket)
```bash
cd backend
python3 manage.py runserver
# Works for REST API, but WebSocket connections will fail
```

### With Redis (Full ASGI + WebSocket)

#### Option A: Uvicorn (Recommended)
```bash
cd backend
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload
```

#### Option B: Daphne
```bash
cd backend
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

#### Option C: Use the script
```bash
./run_asgi.sh
```

## ✅ Test WebSocket Setup

Once Redis is running:
```bash
cd backend
python3 manage.py test_websocket
# Should show: ✓ All tests passed!
```

## 📡 Frontend Connection

Update your frontend to use WebSocket:
```javascript
// In your React app
const token = localStorage.getItem('access_token');
const ws = new WebSocket(`ws://localhost:8000/ws/dashboard/?token=${token}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

## 🔧 Environment Variables

Add to `backend/.env`:
```bash
REDIS_URL=redis://localhost:6379/0
```

For production:
```bash
# Railway/Render automatically sets this
REDIS_URL=redis://user:password@host:port/0
```

## 📊 Current Status

| Component | Status |
|-----------|--------|
| Django ASGI | ✅ Ready |
| Django Channels | ✅ Installed |
| channels-redis | ✅ Installed |
| Daphne | ✅ Installed |
| Uvicorn | ✅ Installed |
| Redis Server | ❌ Not Running |
| WebSocket Consumers | ✅ Ready |
| Frontend Hooks | ✅ Ready |

## 🎯 Next Actions

1. **Install Redis** (choose one option above)
2. **Test setup**: `python3 manage.py test_websocket`
3. **Run server**: `uvicorn config.asgi:application --reload`
4. **Connect frontend**: Use WebSocket hook from `src/hooks/useWebSocket.js`
5. **Integrate notifications**: Add real-time updates to your views

## 📚 Documentation

- [ASGI_CONVERSION_COMPLETE.md](../ASGI_CONVERSION_COMPLETE.md) - Full implementation details
- [WEBSOCKET_SETUP.md](WEBSOCKET_SETUP.md) - Usage guide
- [examples.py](apps/realtime/examples.py) - Integration examples

---

**Everything is ready except Redis. Install it and you're live!**
