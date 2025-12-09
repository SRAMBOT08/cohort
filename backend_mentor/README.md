# Mentor Backend - Cohort Management System

Django backend for the mentor portal of the cohort management system.

## Features

- **Student Tracking**: Monitor assigned students and their progress
- **Submission Review**: Review and grade student submissions
- **Mentor Reports**: Generate progress and performance reports
- **Communication**: Messaging and announcements to students

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
python manage.py runserver 8002
```

## API Documentation

- Swagger UI: http://localhost:8002/api/docs/
- ReDoc: http://localhost:8002/api/docs/redoc/

## API Endpoints

- `/api/students/` - Student tracking and management
- `/api/submissions/` - Submission review and grading
- `/api/reports/` - Mentor reports and analytics
- `/api/communication/` - Messaging and communication
