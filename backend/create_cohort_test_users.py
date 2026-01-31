"""
Create standard test users for cohort application
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

def create_or_update_user(username, email, password, role, first_name='', last_name='', campus='TECH', floor=2):
    """Create or update a user with profile"""
    
    # Try to find user by email or username
    user = None
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        print(f"✓ User exists (by email): {email}")
    elif User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        # Update email if different
        if user.email != email:
            user.email = email
            print(f"✓ User exists (by username): {username}, updating email to {email}")
        else:
            print(f"✓ User exists (by username): {username}")
    else:
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        print(f"✓ Created user: {email}")
    
    # Update password and names
    user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    print(f"  - Password and details updated")
    
    # Update or create profile
    try:
        profile = user.profile
        profile.role = role
        profile.campus = campus if role in ['MENTOR', 'FLOOR_WING', 'STUDENT'] else None
        profile.floor = floor if role in ['MENTOR', 'FLOOR_WING', 'STUDENT'] else None
        profile.save()
        print(f"  - Profile updated: {role}")
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(
            user=user,
            role=role,
            campus=campus if role in ['MENTOR', 'FLOOR_WING', 'STUDENT'] else None,
            floor=floor if role in ['MENTOR', 'FLOOR_WING', 'STUDENT'] else None
        )
        print(f"  - Profile created: {role}")
    
    return user


print(f"\n{'='*60}")
print(f"Creating Standard Test Users")
print(f"{'='*60}\n")

# Create admin
print("1. Admin User:")
admin_user = create_or_update_user(
    username='admin',
    email='admin@cohort.com',
    password='admin123',
    role='ADMIN',
    first_name='Admin',
    last_name='User'
)

# Create mentor
print("\n2. Mentor User:")
mentor_user = create_or_update_user(
    username='mentor1',
    email='mentor1@cohort.com',
    password='mentor123',
    role='MENTOR',
    first_name='Mentor',
    last_name='One',
    campus='TECH',
    floor=2
)

# Create floor wing
print("\n3. Floor Wing User:")
floorwing_user = create_or_update_user(
    username='floorwing1',
    email='floorwing1@cohort.com',
    password='floorwing123',
    role='FLOOR_WING',
    first_name='Floor Wing',
    last_name='One',
    campus='TECH',
    floor=2
)

# Create student
print("\n4. Student User:")
student_user = create_or_update_user(
    username='student1',
    email='student@cohort.com',
    password='pass123#',
    role='STUDENT',
    first_name='Student',
    last_name='One',
    campus='TECH',
    floor=2
)

# Assign student to mentor
student_profile = student_user.profile
student_profile.assigned_mentor = mentor_user
student_profile.save()
print(f"  - Assigned to mentor: {mentor_user.username}")

print(f"\n{'='*60}")
print(f"Test Users Created Successfully!")
print(f"{'='*60}")
print(f"\nCredentials:")
print(f"  Admin:      admin@cohort.com      / admin123")
print(f"  Mentor:     mentor1@cohort.com    / mentor123")
print(f"  Floor Wing: floorwing1@cohort.com / floorwing123")
print(f"  Student:    student@cohort.com    / pass123#")
print(f"{'='*60}\n")
