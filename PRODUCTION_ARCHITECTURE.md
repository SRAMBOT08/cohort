# Production Architecture: Django ASGI + React + Redis

## Overview

This document outlines the production-grade architecture for the Cohort Web Application, transitioning from a traditional WSGI-based Django application to a modern ASGI architecture with real-time capabilities.

## Architecture Components

### Current State
- **Backend**: Django 4.2.7 with WSGI (development server)
- **Frontend**: React with Vite (polling-based updates)
- **Database**: PostgreSQL
- **Deployment**: Traditional request-response cycle

### Target State
- **Backend**: Django ASGI with Channels
- **Frontend**: React with WebSocket support
- **Database**: PostgreSQL
- **Cache/Message Broker**: Redis
- **Real-time**: WebSocket-based live updates

---

## 1. ASGI and WebSocket Support

### ASGI vs WSGI

**WSGI (Web Server Gateway Interface)**
- Synchronous protocol for Python web applications
- One request → one response model
- Cannot maintain persistent connections
- Limited to HTTP request/response cycle

**ASGI (Asynchronous Server Gateway Interface)**
- Asynchronous protocol supporting modern web requirements
- Supports HTTP, HTTP/2, and WebSocket protocols
- Maintains persistent bi-directional connections
- Handles both synchronous and asynchronous code

### Django Channels Integration

Django Channels extends Django to handle protocols beyond HTTP, particularly WebSockets.

**Core Concepts:**

1. **Channel Layer**: Message passing system enabling communication between different parts of the application
2. **Consumers**: WebSocket equivalents of Django views, handling connections and messages
3. **Routing**: URL routing for WebSocket connections, similar to HTTP URL patterns
4. **Groups**: Broadcasting mechanism to send messages to multiple WebSocket connections

### WebSocket Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Browser (React)                   │
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │  HTTP/REST   │         │  WebSocket   │                  │
│  │  API Calls   │         │  Connection  │                  │
│  └──────┬───────┘         └──────┬───────┘                  │
│         │                        │                           │
└─────────┼────────────────────────┼───────────────────────────┘
          │                        │
          ▼                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   ASGI Server (Uvicorn/Daphne)              │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Django Application Layer                 │   │
│  │                                                        │   │
│  │  ┌────────────────┐      ┌─────────────────────┐    │   │
│  │  │  HTTP Views    │      │  WebSocket          │    │   │
│  │  │  (REST API)    │      │  Consumers          │    │   │
│  │  └────────┬───────┘      └──────┬──────────────┘    │   │
│  │           │                     │                     │   │
│  │           │    ┌────────────────┴────────────┐       │   │
│  │           │    │   Channel Layer (Redis)     │       │   │
│  │           │    │   - Message Queue           │       │   │
│  │           │    │   - Group Management        │       │   │
│  │           │    │   - Broadcasting            │       │   │
│  │           │    └────────────┬────────────────┘       │   │
│  │           │                 │                         │   │
│  │           ▼                 ▼                         │   │
│  │  ┌────────────────────────────────────────────┐     │   │
│  │  │          PostgreSQL Database               │     │   │
│  │  └────────────────────────────────────────────┘     │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Real-Time Update Flow (Without Polling)

**Traditional Polling Approach (Current):**
```
Frontend → Poll every 5 seconds → Backend → Database → Response
[Wasteful: 95% of requests return "no changes"]
```

**WebSocket Approach (Target):**
```
1. Frontend establishes WebSocket connection
2. Backend event occurs (new data, update, notification)
3. Backend pushes message through Channel Layer
4. Channel Layer broadcasts to relevant WebSocket groups
5. Frontend receives instant update
6. UI updates automatically
```

**Example Flow: Dashboard Live Updates**

1. Student submits assignment via REST API
2. Django view processes submission, saves to database
3. View sends message to Channel Layer: `assignment.submitted`
4. Channel Layer identifies "mentor_dashboard" group
5. All mentors with open dashboard connections receive update
6. Mentor dashboards update in real-time without refresh

---

## 2. Redis as Message Broker and Cache

### Dual Purpose Architecture

Redis serves two critical functions in this architecture:

#### A. Message Broker for Django Channels

**Purpose**: Enable inter-process communication for WebSocket message distribution

**Function:**
- Stores temporary messages in memory
- Routes messages between Django workers and consumers
- Manages WebSocket group memberships
- Ensures messages reach all connected clients

**Benefits:**
- Sub-millisecond message delivery
- Scalable across multiple application servers
- Persistent connection state management

#### B. Cache Layer

**Purpose**: Reduce database load and improve response times

**Cached Data Examples:**
- User session data
- Dashboard analytics summaries
- Frequently accessed leaderboard rankings
- Student profile aggregations
- Mentor assignment counts

**Cache Strategy:**
```
Request Flow with Redis Cache:

1. Client requests leaderboard data
2. Backend checks Redis: "leaderboard:weekly"
3. If cache hit: Return immediately (< 1ms)
4. If cache miss:
   - Query PostgreSQL (50-200ms)
   - Compute rankings
   - Store in Redis with TTL (60 seconds)
   - Return to client
5. Subsequent requests served from cache
```

### Redis Communication Flow

```
┌──────────────────────────────────────────────────────────┐
│                    Redis Instance                         │
│                                                            │
│  ┌────────────────────┐    ┌──────────────────────┐     │
│  │  Channel Layer     │    │   Cache Storage      │     │
│  │  (Messages/Groups) │    │   (Key-Value Store)  │     │
│  └─────────┬──────────┘    └──────────┬───────────┘     │
│            │                           │                  │
└────────────┼───────────────────────────┼──────────────────┘
             │                           │
     ┌───────┴────────┐         ┌────────┴────────┐
     │                │         │                 │
     ▼                ▼         ▼                 ▼
┌─────────┐    ┌─────────┐  ┌─────────┐    ┌─────────┐
│ Django  │    │ Django  │  │  REST   │    │ Celery  │
│Consumer │    │Consumer │  │   API   │    │ Worker  │
│ Worker  │    │ Worker  │  │  Layer  │    │(Optional)│
└─────────┘    └─────────┘  └─────────┘    └─────────┘
```

**Key Interactions:**

1. **API ↔ Redis Cache**
   - API checks cache before database queries
   - API writes computed results to cache
   - Cache invalidation on data updates

2. **Consumer ↔ Redis Channel Layer**
   - Consumers subscribe to groups via Redis
   - Messages published to Redis are broadcast
   - Redis manages multi-server coordination

3. **Analytics ↔ Redis**
   - Background tasks cache aggregate data
   - Real-time metrics stored temporarily
   - Reduces repeated complex queries

---

## 3. Data Flow and System Design

### Event-Driven Architecture

#### Scenario: Student Submits Assignment

**Complete Flow:**

```
Step 1: Initial Submission
┌─────────────┐
│   React     │  POST /api/assignments/submit
│  Frontend   │  ────────────────────────────┐
└─────────────┘                              │
                                             ▼
                                    ┌─────────────────┐
                                    │   Django View   │
                                    │   (REST API)    │
                                    └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │   PostgreSQL    │
                                    │   [Write Data]  │
                                    └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Invalidate Cache│
                                    │ (Student Stats) │
                                    └────────┬────────┘
                                             │
Step 2: Broadcast Update                    ▼
                                    ┌─────────────────┐
                                    │ Channel Layer   │
                        ┌───────────┤ Send Message    │───────────┐
                        │           │ to Groups:      │           │
                        │           │ - mentor_X      │           │
                        │           │ - admin_panel   │           │
                        │           │ - student_Y     │           │
                        │           └─────────────────┘           │
                        │                                          │
                        ▼                                          ▼
              ┌──────────────────┐                      ┌──────────────────┐
              │ Mentor Dashboard │                      │ Admin Dashboard  │
              │  [WebSocket]     │                      │   [WebSocket]    │
              │ "New submission  │                      │ "New submission" │
              │  from Student Y" │                      │                  │
              └──────────────────┘                      └──────────────────┘

Step 3: Dashboard Refresh
              ┌──────────────────┐
              │  React Component │
              │  receives message│
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  Fetch Updated   │
              │  Data via REST   │
              │  (from cache)    │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   UI Updates     │
              │   Automatically  │
              └──────────────────┘
```

### Database Load Reduction with Redis

**Problem Without Cache:**
- Dashboard loads require complex JOIN queries
- Leaderboard recalculates rankings on each request
- 1000 concurrent users = 1000 database queries/second
- Database becomes bottleneck at scale

**Solution With Redis:**
```
Database Load Comparison:

Without Redis:
- Dashboard load: 5 DB queries × 200ms = 1000ms
- 1000 users/minute = 5000 queries/minute
- Database CPU: 80-95%

With Redis:
- First request: 5 DB queries × 200ms = 1000ms → Cache
- Subsequent requests: 1 Redis query × 1ms = 1ms
- Cache hit ratio: 95%
- Database queries: 250/minute (95% reduction)
- Database CPU: 10-15%
```

**Cache Invalidation Strategy:**

1. **Time-Based Expiration**
   - Leaderboard: 60 seconds
   - User stats: 120 seconds
   - Activity feed: 30 seconds

2. **Event-Based Invalidation**
   - On data update: Clear relevant cache keys
   - On submission: Invalidate student and mentor caches
   - On grade update: Clear leaderboard cache

3. **Pattern-Based Invalidation**
   - Clear all keys matching pattern: `student:123:*`
   - Bulk invalidation for related entities

### Scalability Analysis

**Single Server (Current WSGI):**
```
Capacity: ~100 concurrent users
Bottleneck: Synchronous request handling
Polling overhead: 10 requests/second per user
```

**Multi-Server ASGI with Redis (Target):**
```
Capacity: 10,000+ concurrent users
Horizontal scaling: Add more application servers
Redis handles inter-server communication
WebSocket connections distributed across servers

Scaling Pattern:
1-1000 users: 1 application server + 1 Redis instance
1000-5000 users: 3 application servers + 1 Redis instance
5000-20000 users: 8 application servers + Redis cluster
```

**Load Distribution:**
```
┌───────────────┐
│ Load Balancer │
└───────┬───────┘
        │
   ┌────┴────┬────────────┬───────────┐
   ▼         ▼            ▼           ▼
┌──────┐  ┌──────┐    ┌──────┐    ┌──────┐
│App-1 │  │App-2 │    │App-3 │    │App-N │
└──┬───┘  └──┬───┘    └──┬───┘    └──┬───┘
   │         │            │            │
   └─────────┴────────────┴────────────┘
                   │
                   ▼
         ┌──────────────────┐
         │  Redis Cluster   │
         │  (Shared State)  │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │    PostgreSQL    │
         │   (Primary DB)   │
         └──────────────────┘
```

---

## 4. Deployment Considerations

### Infrastructure Requirements

#### Minimum Production Stack

1. **ASGI Application Server**
   - Uvicorn or Daphne
   - Process manager (Supervisor, systemd, PM2)
   - Multiple workers for load distribution
   - Memory: 512MB minimum per worker

2. **Redis Service**
   - Dedicated Redis instance or cluster
   - Memory: 256MB minimum (scales with users)
   - Persistence configuration for message durability
   - Network latency < 5ms from application servers

3. **PostgreSQL Database**
   - Connection pooling (PgBouncer recommended)
   - Adequate connections for concurrent workers
   - Read replicas for analytics queries (optional)

4. **Web Server / Load Balancer**
   - Nginx or similar for SSL termination
   - WebSocket proxy support (`proxy_pass` with upgrade headers)
   - Static file serving
   - Request routing to application servers

### Why Traditional Shared Hosting is Insufficient

**Shared Hosting Limitations:**

1. **No ASGI Support**
   - Shared hosting runs Apache/Nginx with PHP or WSGI only
   - Cannot maintain persistent WebSocket connections
   - No process management for ASGI workers

2. **No Redis Access**
   - Shared hosting provides MySQL/MariaDB only
   - No in-memory data stores
   - Cannot install additional services

3. **Resource Constraints**
   - Limited concurrent connections
   - Shared CPU/memory with other tenants
   - No control over process management
   - Cannot configure reverse proxy for WebSockets

4. **Networking Restrictions**
   - WebSocket connections often blocked
   - No persistent connection support
   - Limited ports and protocols

**Required Hosting Types:**

✅ **VPS (Virtual Private Server)**
- Full control over services
- Can install Redis, Uvicorn
- Configure Nginx for WebSocket proxy
- Examples: DigitalOcean Droplets, Linode, AWS EC2

✅ **Platform-as-a-Service (PaaS)**
- Managed infrastructure
- Built-in Redis support
- ASGI/WebSocket support
- Examples: Railway, Render, Heroku (with Redis add-on), AWS Elastic Beanstalk

✅ **Container Platforms**
- Docker-based deployments
- Orchestration with Kubernetes
- Microservices architecture
- Examples: AWS ECS/Fargate, Google Cloud Run, Azure Container Apps

### Production Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   DNS / CDN     │
                │   SSL/TLS       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Load Balancer  │
                │  (Nginx/HAProxy)│
                └────────┬────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │ ASGI   │      │ ASGI   │      │ ASGI   │
    │Server 1│      │Server 2│      │Server N│
    │(Uvicorn)      │(Uvicorn)      │(Uvicorn)
    └───┬────┘      └───┬────┘      └───┬────┘
        │               │               │
        └───────────────┴───────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
    ┌───────────────┐      ┌──────────────┐
    │ Redis Cluster │      │  PostgreSQL  │
    │ - Channel Lyr │      │  Primary DB  │
    │ - Cache       │      │              │
    └───────────────┘      └──────────────┘
```

### Service Configuration Overview

**ASGI Server:**
```
- Workers: (CPU cores × 2) + 1
- Timeout: 60 seconds for WebSocket connections
- Max connections: 1000 per worker
- Graceful shutdown: 30 seconds
```

**Redis Configuration:**
```
- Max memory: 2GB (adjust based on load)
- Eviction policy: allkeys-lru for cache
- Persistence: AOF for message durability
- Connection pool: 50 connections per app worker
```

**Database Connections:**
```
- Connection pool: 20-50 per app worker
- Query timeout: 30 seconds
- Connection lifetime: 3600 seconds
- Prepared statement cache: enabled
```

**Nginx WebSocket Proxy:**
```
- Proxy timeout: 600 seconds
- WebSocket upgrade headers required
- Connection keep-alive
- Buffer size: 64k
```

### Monitoring Requirements

**Key Metrics to Track:**

1. **WebSocket Connections**
   - Active connections per server
   - Connection duration
   - Message throughput

2. **Redis Performance**
   - Memory usage
   - Cache hit ratio
   - Commands per second
   - Eviction count

3. **Database Performance**
   - Query execution time
   - Connection pool utilization
   - Slow query log
   - Index usage

4. **Application Metrics**
   - Request latency (HTTP and WebSocket)
   - Error rates
   - Memory usage per worker
   - CPU utilization

---

## Migration Path

### Phase 1: Add Redis Cache (Low Risk)
- Install Redis service
- Implement cache layer for read-heavy queries
- No frontend changes required
- Immediate performance improvement

### Phase 2: Deploy ASGI (Medium Risk)
- Switch from WSGI to ASGI server
- No code changes to existing HTTP views
- Test all existing functionality
- Fallback to WSGI if issues occur

### Phase 3: Implement WebSocket Consumers (High Value)
- Add Django Channels
- Configure Redis as channel layer
- Create WebSocket consumers for real-time features
- Update frontend to establish WebSocket connections

### Phase 4: Optimize and Scale (Ongoing)
- Add more application servers
- Implement Redis cluster
- Database read replicas
- Advanced caching strategies

---

## Security Considerations

### WebSocket Authentication
- Token-based authentication for WebSocket connections
- Validate tokens before establishing connection
- Automatic disconnection on token expiration

### Redis Security
- Firewall rules: Only application servers can access
- Password authentication enabled
- No public internet access
- Separate Redis instances for cache vs channel layer (optional)

### Rate Limiting
- Limit WebSocket message frequency per connection
- Throttle REST API requests
- Protect against connection flooding

---

## Cost Implications

**Shared Hosting (Current Potential):**
- Cost: $5-10/month
- Limitations: Cannot support target architecture

**VPS Deployment (Minimum):**
- Application server: 2GB RAM, 2 CPU cores: $12-20/month
- Redis: 1GB RAM: $10-15/month
- PostgreSQL: Managed service: $15-25/month
- **Total: $37-60/month**

**PaaS Deployment (Recommended for Simplicity):**
- Application dyno: $25-50/month
- Redis add-on: $15-30/month
- PostgreSQL add-on: $9-50/month
- **Total: $49-130/month**

**Scaling Costs:**
- Additional application servers: ~$25/month each
- Redis cluster: ~$50-100/month
- Database scaling: ~$50-200/month

---

## Performance Benefits Summary

| Metric | Current (WSGI) | Target (ASGI + Redis) | Improvement |
|--------|---------------|---------------------|-------------|
| Dashboard Load Time | 2-3 seconds | 100-300ms | 10x faster |
| Real-time Updates | 5-30 second delay | < 100ms | 50-300x faster |
| Database Load | High (constant polling) | Low (event-driven) | 90% reduction |
| Concurrent Users | ~100 | 5000+ | 50x capacity |
| Server Response | 200-500ms | 50-150ms | 3-4x faster |

---

## Conclusion

This architecture transformation enables:

1. **Real-time interactivity** without polling overhead
2. **Horizontal scalability** through stateless application servers
3. **Reduced infrastructure costs** through efficient caching
4. **Better user experience** with instant updates
5. **Production-grade foundation** for future growth

The investment in ASGI, WebSockets, and Redis creates a modern, scalable platform capable of supporting thousands of concurrent users with minimal latency.
