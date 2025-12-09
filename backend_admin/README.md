# Admin Backend - Cohort Management System

Django backend for the admin portal of the cohort management system.

## Features

- **User Management**: Manage students, mentors, and admin users
- **Mentor Management**: Assign mentors, track mentor performance
- **Cohort Management**: Create and manage cohort groups
- **Analytics & Reporting**: System-wide analytics and reporting

## Tech Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL
- JWT Authentication
- Swagger/OpenAPI Documentation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run server:
```bash
python manage.py runserver 8001
```

## API Documentation

- Swagger UI: http://localhost:8001/api/docs/
- ReDoc: http://localhost:8001/api/docs/redoc/

## API Endpoints

- `/api/users/` - User management
- `/api/mentors/` - Mentor management
- `/api/cohorts/` - Cohort management
- `/api/analytics/` - Analytics and reporting
