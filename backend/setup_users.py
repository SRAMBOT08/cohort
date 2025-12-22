#!/usr/bin/env python
"""
Setup script to create admin, mentor, floor wing and import students from CSV
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

def create_admin():
    """Create an admin user"""
    username = 'admin'
    email = 'admin@snsce.ac.in'
    password = 'admin123'
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, email=email, password=password)
        
        # Create or update profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = 'ADMIN'
        profile.save()
        
        print(f'✅ Admin "{username}" created successfully!')
    else:
        print(f'ℹ️  Admin "{username}" already exists.')

def create_mentor():
    """Create a mentor user"""
    username = 'mentor'
    email = 'mentor@snsce.ac.in'
    password = 'mentor123'
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.save()
        
        # Create or update profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = 'MENTOR'
        profile.campus = 'TECH'
        profile.floor = 1
        profile.save()
        
        print(f'✅ Mentor "{username}" created successfully!')
    else:
        print(f'ℹ️  Mentor "{username}" already exists.')

def create_floorwing():
    """Create a floor wing user"""
    username = 'floorwing'
    email = 'floorwing@snsce.ac.in'
    password = 'floorwing123'
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.save()
        
        # Create or update profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = 'FLOOR_WING'
        profile.campus = 'TECH'
        profile.floor = 1
        profile.save()
        
        print(f'✅ Floor Wing "{username}" created successfully!')
    else:
        print(f'ℹ️  Floor Wing "{username}" already exists.')

def import_users_from_csv():
    """Import users from dummy CSV file"""
    # Check multiple possible paths
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'dummy users - Sheet1.csv'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dummy users - Sheet1.csv'),
        '/opt/render/project/src/dummy users - Sheet1.csv',
        '/opt/render/project/src/backend/dummy users - Sheet1.csv',
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if not csv_path:
        print(f'⚠️  CSV file not found. Creating demo students instead...')
        create_demo_students()
        return
    
    created_count = 0
    skipped_count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row['email'].strip()
            username = row['username'].strip()
            password = row['password'].strip()
            
            user = None
            if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                # Ensure we fetch the user and reset password/role to keep creds in sync with CSV
                user = User.objects.filter(email=email).first() or User.objects.filter(username=username).first()
                skipped_count += 1
                user.set_password(password)
                user.username = username  # ensure username matches CSV
                user.email = email
                user.save()
            else:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                created_count += 1
            
            # Create/update profile as student
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = 'STUDENT'
            profile.campus = 'TECH'
            profile.floor = 1
            profile.save()
    
    print(f'✅ Imported {created_count} users from CSV (skipped {skipped_count} existing)')

def create_demo_students():
    """Create demo students if CSV not available"""
    students = [
        ('student1', 'student1@snsce.ac.in', 'student123'),
        ('student2', 'student2@snsce.ac.in', 'student123'),
        ('student3', 'student3@snsce.ac.in', 'student123'),
        ('student4', 'student4@snsce.ac.in', 'student123'),
        ('student5', 'student5@snsce.ac.in', 'student123'),
    ]
    
    created_count = 0
    for username, email, password in students:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = 'STUDENT'
            profile.campus = 'TECH'
            profile.floor = 1
            profile.save()
            created_count += 1
    
    print(f'✅ Created {created_count} demo students')

if __name__ == '__main__':
    print('👤 Setting up users...')
    create_admin()
    create_mentor()
    create_floorwing()
    import_users_from_csv()
    print('✅ User setup complete!')
