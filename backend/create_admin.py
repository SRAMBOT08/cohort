#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@cohort.com',
        password='admin123'
    )
    print('✓ Superuser created successfully!')
    print('')
    print('Login credentials:')
    print('  Username: admin')
    print('  Password: admin123')
    print('')
    print('Access Django Admin at:')
    print('  http://127.0.0.1:8001/admin/')
else:
    print('✓ Superuser already exists')
    print('')
    print('Credentials:')
    print('  Username: admin')
    print('  Password: admin123')
    print('')
    print('Access at: http://127.0.0.1:8001/admin/')
