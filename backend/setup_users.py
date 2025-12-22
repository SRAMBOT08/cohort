#!/usr/bin/env python
"""
Setup script to create mentor and import users from CSV
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.profiles.models import UserProfile
import csv

User = get_user_model()

def create_mentor():
    """Create a mentor user"""
    username = os.getenv('MENTOR_USERNAME', 'mentor')
    email = os.getenv('MENTOR_EMAIL', 'mentor@snsce.ac.in')
    password = os.getenv('MENTOR_PASSWORD', 'mentor123')
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.save()
        
        # Create or update profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = 'mentor'
        profile.save()
        
        print(f'✅ Mentor "{username}" created successfully!')
    else:
        print(f'ℹ️  Mentor "{username}" already exists.')

def import_users_from_csv():
    """Import users from dummy CSV file"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dummy users - Sheet1.csv')
    
    if not os.path.exists(csv_path):
        print(f'⚠️  CSV file not found at {csv_path}')
        return
    
    created_count = 0
    skipped_count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row['email'].strip()
            username = row['username'].strip()
            password = row['password'].strip()
            
            if User.objects.filter(email=email).exists():
                skipped_count += 1
                continue
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create profile as student
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = 'student'
            profile.save()
            
            created_count += 1
    
    print(f'✅ Imported {created_count} users from CSV (skipped {skipped_count} existing)')

if __name__ == '__main__':
    print('👤 Setting up users...')
    create_mentor()
    import_users_from_csv()
    print('✅ User setup complete!')
