#!/usr/bin/env python
"""Simple script to import users - run with: python import_users_simple.py"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile
import csv

def main():
    print("Starting import...")
    
    # First, create admin if doesn't exist
    admin_email = "admin@test.com"
    if not User.objects.filter(email=admin_email).exists():
        admin = User.objects.create_superuser(
            username='admin',
            email=admin_email,
            password='admin123'
        )
        print(f"✅ Created admin user: {admin_email}")
    else:
        print(f"✅ Admin user already exists: {admin_email}")
    
    # Import CSV users
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'dummy users - Sheet1.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV not found: {csv_path}")
        return
    
    campus = 'TECH'
    floor = 2
    created = 0
    updated = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row['email'].strip()
            username = row['username'].strip()
            
            user, is_new = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': username.split()[0] if username else '',
                    'last_name': ' '.join(username.split()[1:]) if len(username.split()) > 1 else ''
                }
            )
            
            user.set_password('pass123#')
            user.save()
            
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'STUDENT', 'campus': campus, 'floor': floor}
            )
            profile.role = 'STUDENT'
            profile.campus = campus
            profile.floor = floor
            profile.save()
            
            if is_new:
                created += 1
            else:
                updated += 1
            
            print(f"{'✅ Created' if is_new else '🔄 Updated'}: {username} ({email})")
    
    print(f"\n✅ Import complete!")
    print(f"Created: {created}, Updated: {updated}, Total: {created + updated}")

if __name__ == '__main__':
    main()
