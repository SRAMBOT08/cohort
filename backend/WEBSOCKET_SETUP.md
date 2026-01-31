# Real-Time WebSocket Integration - Quick Start

## Installation

Install new dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Add to your `.env` file:
```bash
# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# For production (Railway, Render, etc.)
# REDIS_URL=redis://user:password@host:port/0
```

## Running the Server

### Development (Daphne - ASGI server):
```bash
cd backend
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

### Production (Uvicorn):
```bash
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers 4
```

### Alternative (Daphne with workers):
```bash
daphne -b 0.0.0.0 -p 8000 -w 4 config.asgi:application
```

## WebSocket Endpoints

### Available WebSocket URLs:

1. **Dashboard Updates** (Admin/Mentor)
   - `ws://localhost:8000/ws/dashboard/?token=YOUR_JWT_TOKEN`

2. **Personal Notifications**
   - `ws://localhost:8000/ws/notifications/?token=YOUR_JWT_TOKEN`

3. **Leaderboard Updates**
   - `ws://localhost:8000/ws/leaderboard/?token=YOUR_JWT_TOKEN`

4. **Mentor-Specific Updates**
   - `ws://localhost:8000/ws/mentor/{mentor_id}/?token=YOUR_JWT_TOKEN`

5. **Student-Specific Updates**
   - `ws://localhost:8000/ws/student/{student_id}/?token=YOUR_JWT_TOKEN`

## Frontend Integration (React)

### Example: Connect to WebSocket
```javascript
// Get JWT token from your auth system
const token = localStorage.getItem('access_token');

// Connect to WebSocket
const ws = new WebSocket(`ws://localhost:8000/ws/dashboard/?token=${token}`);

ws.onopen = () => {
  console.log('Connected to dashboard');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'submission_created':
      // Update UI with new submission
      console.log('New submission:', data.submission);
      break;
    case 'grade_updated':
      // Update UI with grade
      console.log('Grade updated:', data.grade);
      break;
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from dashboard');
};
```

### Example: React Hook
```javascript
import { useEffect, useState } from 'react';

function useDashboardWebSocket(token) {
  const [data, setData] = useState([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!token) return;

    const ws = new WebSocket(`ws://localhost:8000/ws/dashboard/?token=${token}`);

    ws.onopen = () => setConnected(true);
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setData(prev => [...prev, message]);
    };

    ws.onclose = () => setConnected(false);

    return () => ws.close();
  }, [token]);

  return { data, connected };
}
```

## Backend Integration - Sending Real-Time Updates

### From REST API Views
```python
from apps.realtime.utils import notify_student, update_leaderboard

# In your view/viewset
def grade_submission(request, submission_id):
    # ... your grading logic ...
    
    # Send real-time notification
    notify_student(
        submission.student.id,
        'grade_received',
        {
            'grade': {
                'assignment': submission.assignment.title,
                'score': submission.grade,
                'feedback': submission.feedback
            }
        }
    )
    
    return Response({'status': 'graded'})
```

### From Signal Handlers
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.realtime.utils import notify_dashboard

@receiver(post_save, sender=YourModel)
def model_saved(sender, instance, created, **kwargs):
    if created:
        notify_dashboard('model_created', {
            'id': instance.id,
            'name': str(instance)
        })
```

### From Background Tasks/Celery
```python
from apps.realtime.utils import update_leaderboard

def calculate_leaderboard_task():
    # Calculate leaderboard
    leaderboard = [...]
    
    # Broadcast to all connected clients
    update_leaderboard(leaderboard)
```

## Testing WebSocket Connections

### Using wscat (CLI tool):
```bash
npm install -g wscat
wscat -c "ws://localhost:8000/ws/dashboard/?token=YOUR_JWT"
```

### Using Python:
```python
import asyncio
import websockets

async def test_connection():
    uri = "ws://localhost:8000/ws/dashboard/?token=YOUR_JWT"
    async with websockets.connect(uri) as websocket:
        message = await websocket.recv()
        print(f"Received: {message}")

asyncio.run(test_connection())
```

## Production Deployment

### Required Services:
1. **Redis** - Must be available and configured
2. **ASGI Server** - Daphne or Uvicorn
3. **Process Manager** - systemd, Supervisor, or PM2

### Environment Variables:
```bash
REDIS_URL=redis://your-redis-host:6379/0
ALLOWED_HOSTS=yourdomain.com
```

### Nginx Configuration for WebSocket:
```nginx
location /ws/ {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 86400;
}
```

## Monitoring

Check Redis connection:
```bash
python manage.py shell
>>> from channels.layers import get_channel_layer
>>> channel_layer = get_channel_layer()
>>> await channel_layer.send('test_channel', {'type': 'test.message'})
```
