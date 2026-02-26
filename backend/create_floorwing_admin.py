#!/usr/bin/env python3
"""
Create Floor Wing Admin User for Tech 2nd Floor
Run this script in Render shell: python create_floorwing_admin.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.profiles.models import UserProfile

User = get_user_model()

print("=" * 60)
print("CREATING FLOOR WING ADMIN USER")
print("=" * 60)

# Floor Wing details
username = 'Reshma Raj'
email = 'reshma.r.dt@snsgroups.com'
password = 'FloorWing@Tech2'  # Change this to a secure password
campus = 'TECH'
floor = 2
role = 'FLOOR_WING'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"⚠️  User '{username}' already exists!")
    user = User.objects.get(username=username)
    print(f"   Email: {user.email}")
    
    # Update the user's profile
    profile = user.profile
    profile.role = role
    profile.campus = campus
    profile.floor = floor
    profile.save()
    print(f"✓  Updated profile to Floor Wing - Tech 2nd Floor")
    
    # Reset password
    user.set_password(password)
    user.save()
    print(f"✓  Password reset")
else:
    # Create new user
    print(f"Creating user: {username}")
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Floor Wing',
        last_name='Tech 2nd Floor'
    )
    print(f"✓  User created: {username}")
    
    # Update profile
    profile = user.profile
    profile.role = role
    profile.campus = campus
    profile.floor = floor
    profile.save()
    print(f"✓  Profile updated")

print("\n" + "=" * 60)
print("FLOOR WING ADMIN CREATED SUCCESSFULLY!")
print("=" * 60)
print(f"Username: {username}")
print(f"Email:    {email}")
print(f"Password: {password}")
print(f"Role:     {role}")
print(f"Campus:   {campus} (SNS College of Technology)")
print(f"Floor:    {floor} (2nd Year)")
print("=" * 60)
print("\nThis user can now:")
print("  • Create and manage seasons")
print("  • Create and manage episodes")
print("  • Configure gamification settings")
print("\nAPI Endpoints available:")
print("  POST /api/gamification/floorwing/seasons/")
print("  GET  /api/gamification/floorwing/seasons/")
print("  PUT  /api/gamification/floorwing/seasons/<id>/")
print("  POST /api/gamification/floorwing/seasons/<id>/episodes/")
print("=" * 60)
print("\n⚠️  IMPORTANT: Change the password after first login!")
print("=" * 60)
