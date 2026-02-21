# Cohort Summit Application

A comprehensive platform connecting students, mentors, and institutions through five pillars of holistic development.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react)
![Django](https://img.shields.io/badge/Django-4.2.7-092E20?logo=django)
![Vite](https://img.shields.io/badge/Vite-7.2.4-646CFF?logo=vite)

## Table of Contents
- [Quick Start](#quick-start)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running](#running-the-application)
- [Five Pillars](#five-pillars)
- [API](#api-documentation)
- [Contributing](#contributing)

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL 14+

### Setup

**Frontend:**
```bash
npm install
npm run dev  # http://localhost:5173
```

**Backend:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver  # http://127.0.0.1:8000
```

## Features

| Role | Features |
|------|----------|
| **Student** | Dashboard, pillar submissions, progress tracking, analytics |
| **Mentor** | Review submissions, provide feedback, student tracking, analytics |
| **Admin** | User management, institutional analytics, floor management |
| **Floor Rep** | Dashboard, announcements, local analytics |

## Tech Stack

**Frontend:** React 19, Vite, React Router, Framer Motion, Three.js, Recharts, Zustand

**Backend:** Django 4.2, DRF, JWT Auth, PostgreSQL, Pillow, CORS

## Installation

```bash
# Clone
git clone https://github.com/Amal0318/Cohort_Web_App.git
cd Cohort_Web_App

# Frontend .env
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env

# Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Backend .env
cat > .env << EOF
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=cohort_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
EOF

# Database
psql -U postgres
CREATE DATABASE cohort_db;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE cohort_db TO your_user;

# Migrate
python3 manage.py migrate
python3 manage.py createsuperuser
```

## Running the Application

**Terminal 1 - Frontend:**
```bash
npm run dev
```

**Terminal 2 - Backend:**
```bash
cd backend
source .venv/bin/activate
python3 manage.py runserver
```

**Access:**
- Frontend: http://localhost:5173
- API: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

## Five Pillars

1. **CLT** - Continuous Learning Track (Courses, certifications)
2. **SRI** - Social Responsibility Initiative (Volunteer work, community service)
3. **CFC** - Center for Creativity (Hackathons, projects)
4. **IIPC** - Industry & Interview Prep (LinkedIn, networking)
5. **SCD** - Self-Code Development (LeetCode, GitHub)

## Project Structure

```
cohort/
├── backend/              # Django REST API
│   ├── apps/            # CLT, SRI, CFC, IIPC, SCD apps
│   ├── config/          # Settings, URLs, WSGI
│   └── manage.py
├── src/                 # React frontend
│   ├── components/      # Reusable UI components
│   ├── pages/          # Student, Mentor, Admin pages
│   ├── services/       # API integrations
│   ├── store/          # Zustand state management
│   └── theme/          # Theming
├── docs/               # Documentation
└── public/             # Static assets
```

## API Endpoints

**Authentication:**
```
POST   /api/auth/token/       # Login
POST   /api/auth/token/refresh/
GET    /api/auth/user/
```

**Student:**
```
POST   /api/clt/submissions/
POST   /api/sri/submissions/
POST   /api/cfc/hackathon/
POST   /api/iipc/posts/
POST   /api/scd/submissions/
GET    /api/dashboard/stats/
```

**Mentor:**
```
GET    /api/mentor/students/
GET    /api/mentor/submissions/
POST   /api/mentor/review/
GET    /api/mentor/analytics/
```

**Admin:**
```
GET    /api/admin/users/
POST   /api/admin/users/
PUT    /api/admin/users/{id}/
DELETE /api/admin/users/{id}/
GET    /api/admin/analytics/
```

## Testing

```bash
# Frontend
npm run lint
npm run preview

# Backend
cd backend
python3 manage.py test
python3 test_clt_endpoints.py
python3 test_iipc_endpoints.py
```

## Contributing

1. Create branch: `git checkout -b feature/name`
2. Commit: `git commit -m 'feat: description'`
3. Push: `git push origin feature/name`
4. Open Pull Request

**Branch Strategy:**
- `main` - Production
- `develop` - Development
- `feature/*` - Features
- `bugfix/*` - Fixes

## Environment Variables

**Frontend (.env):**
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_LINKEDIN_CLIENT_ID=your_id
VITE_LINKEDIN_REDIRECT_URI=http://localhost:5173/iipc/callback
```

**Backend (.env):**
```env
DEBUG=True
SECRET_KEY=your-key
DATABASE_NAME=cohort_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_pass
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
JWT_SECRET_KEY=your-jwt-key
```

## Design System

**Colors:**
- Primary: `#F7C948` → `#E53935`
- Background (Light): `#FFFFFF`
- Background (Dark): `#121212`

**Typography:**
- Headings: Sora (700-800)
- Body: Inter (400-600)
- UI: Manrope (500-700)

## Known Issues

- Migration warnings for `clt` app (non-blocking)
- Port 5173 occupied → uses 5174 automatically

## Future Enhancements

- [ ] Mobile app (React Native)
- [ ] WebSocket notifications
- [ ] Advanced analytics
- [ ] AI-powered insights
- [ ] Export reports (PDF/Excel)
- [ ] Gamification

## Support

- **Email**: support@cohortweb.com
- **Issues**: GitHub Issues
- **Docs**: Project Wiki

## License

Proprietary. All rights reserved.

---

**Built with ❤️ by the Cohort Team**

*Updated: February 2026*
