#!/usr/bin/env python3
"""
Create 5 test users mapped to the same floor:
- 1 Admin
- 1 Mentor
- 1 Floor Wing
- 2 Students (both assigned to the mentor)
All on Floor 2, TECH campus
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Configuration
FLOOR = 2
CAMPUS = 'TECH'

# Test user credentials
users_to_create = [
    {
        'username': 'testadmin',
        'email': 'testadmin@cohort.com',
        'password': 'admin@123',
        'first_name': 'Test',
        'last_name': 'Admin',
        'role': 'ADMIN'
    },
    {
        'username': 'testmentor',
        'email': 'testmentor@cohort.com',
        'password': 'mentor@123',
        'first_name': 'Test',
        'last_name': 'Mentor',
        'role': 'MENTOR'
    },
    {
        'username': 'testfloorwing',
        'email': 'testfloorwing@cohort.com',
        'password': 'floorwing@123',
        'first_name': 'Test',
        'last_name': 'FloorWing',
        'role': 'FLOOR_WING'
    },
    {
        'username': 'teststudent1',
        'email': 'teststudent1@cohort.com',
        'password': 'student@123',
        'first_name': 'Test',
        'last_name': 'Student One',
        'role': 'STUDENT',
        'leetcode_id': 'teststudent1',
        'github_id': 'teststudent1'
    },
    {
        'username': 'teststudent2',
        'email': 'teststudent2@cohort.com',
        'password': 'student@123',
        'first_name': 'Test',
        'last_name': 'Student Two',
        'role': 'STUDENT',
        'leetcode_id': 'teststudent2',
        'github_id': 'teststudent2'
    },
]

print("=" * 70)
print("Creating 5 Test Users Mapped to Same Floor")
print("=" * 70)
print(f"Campus: {CAMPUS} (Dr. SNS Rajalakshmi College of Arts and Science)")
print(f"Floor: {FLOOR} (2nd Year)")
print()

created_users = {}

# Step 1: Create all users
print("Step 1: Creating users...")
print("-" * 70)

for user_data in users_to_create:
    username = user_data['username']
    
    # Delete existing user if exists
    User.objects.filter(username=username).delete()
    User.objects.filter(email=user_data['email']).delete()
    
    # Create user
    if user_data['role'] == 'ADMIN':
        user = User.objects.create_superuser(
            username=username,
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
    else:
        user = User.objects.create_user(
            username=username,
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        
        # Give staff access to mentors and floor wings
        if user_data['role'] in ['MENTOR', 'FLOOR_WING']:
            user.is_staff = True
            user.save()
    
    # Create or update profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.role = user_data['role']
    profile.campus = CAMPUS
    profile.floor = FLOOR
    
    # Add platform IDs if provided
    if 'leetcode_id' in user_data:
        profile.leetcode_id = user_data['leetcode_id']
    if 'github_id' in user_data:
        profile.github_id = user_data['github_id']
    if 'linkedin_id' in user_data:
        profile.linkedin_id = user_data['linkedin_id']
    
    profile.save()
    
    created_users[user_data['role']] = user
    
    print(f"✓ Created {user_data['role']}: {user.get_full_name()} ({username})")

print()

# Step 2: Assign students to mentor
print("Step 2: Assigning students to mentor...")
print("-" * 70)

if 'MENTOR' in created_users:
    mentor_user = created_users['MENTOR']
    
    # Get all student profiles on the same floor
    student_profiles = UserProfile.objects.filter(
        role='STUDENT',
        campus=CAMPUS,
        floor=FLOOR
    )
    
    for profile in student_profiles:
        profile.assigned_mentor = mentor_user
        profile.save()
        print(f"✓ Assigned {profile.user.get_full_name()} to mentor {mentor_user.get_full_name()}")

print()

# Display credentials
print("=" * 70)
print("✅ ALL USERS CREATED SUCCESSFULLY!")
print("=" * 70)
print()
print("LOGIN CREDENTIALS:")
print("=" * 70)

for user_data in users_to_create:
    print(f"\n{user_data['role']} ({user_data['first_name']} {user_data['last_name']}):")
    print(f"  Username: {user_data['username']}")
    print(f"  Email:    {user_data['email']}")
    print(f"  Password: {user_data['password']}")
    print(f"  Campus:   {CAMPUS}")
    print(f"  Floor:    {FLOOR}")

print()
print("=" * 70)
print("SUMMARY:")
print("=" * 70)
print(f"• All 5 users are on Floor {FLOOR} of {CAMPUS} campus")
print(f"• Both students are assigned to mentor: {created_users['MENTOR'].get_full_name()}")
print(f"• Admin has full system access")
print(f"• Backend: http://127.0.0.1:8000/")
print(f"• Frontend: http://localhost:5174/")
print("=" * 70)
