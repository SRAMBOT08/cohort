"""
Import students from package-lock.xlsx (mentor wise sheet)
Mentor assignment logic: mentor name appears once, all students below belong to that mentor until next mentor

Run from backend directory: python scripts_archive/import_students_from_package_lock.py
"""
import os
import sys
import django
import pandas as pd

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Configuration
EXCEL_FILE = 'package-lock.xlsx'
SHEET_NAME = 'mentor wise'
DEFAULT_PASSWORD = 'student123'
CAMPUS = 'TECH'
FLOOR = 2

def main():
    print("=" * 80)
    print("IMPORTING STUDENTS FROM PACKAGE-LOCK.XLSX")
    print("=" * 80)
    print(f"\nReading Excel file: {EXCEL_FILE}")
    print(f"Sheet: {SHEET_NAME}\n")
    
    # Read Excel file
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    
    print(f"Total rows in Excel: {len(df)}")
    print(f"Columns: {list(df.columns)}\n")
    
    # Forward fill the mentor column - each mentor applies to all students below until next mentor
    df['mentor_filled'] = df['mentor'].fillna(method='ffill')
    
    # Show mentor distribution
    mentor_counts = df['mentor_filled'].value_counts()
    print("Students per mentor:")
    for mentor, count in mentor_counts.items():
        print(f"  {mentor}: {count} students")
    print()
    
    # Process each student
    created_count = 0
    updated_count = 0
    error_count = 0
    skipped_count = 0
    
    # Get or create mentors first
    mentor_users = {}
    for mentor_name in df['mentor_filled'].unique():
        if pd.notna(mentor_name):
            mentor_username = mentor_name.lower().replace(' ', '_')
            mentor_user, created = User.objects.get_or_create(
                username=mentor_username,
                defaults={
                    'email': f'{mentor_username}@cohortsummit.com',
                    'first_name': mentor_name.split()[0],
                    'last_name': ' '.join(mentor_name.split()[1:]) if len(mentor_name.split()) > 1 else '',
                }
            )
            if created:
                mentor_user.set_password('mentor123')
                mentor_user.save()
                print(f"✅ Created mentor: {mentor_name} (username: {mentor_username})")
            
            # Ensure mentor profile exists
            mentor_profile, _ = UserProfile.objects.get_or_create(user=mentor_user)
            mentor_profile.role = 'MENTOR'
            mentor_profile.campus = CAMPUS
            mentor_profile.floor = FLOOR
            mentor_profile.save()
            
            mentor_users[mentor_name] = mentor_user
    
    print("\n" + "=" * 80)
    print("CREATING STUDENTS")
    print("=" * 80 + "\n")
    
    for idx, row in df.iterrows():
        try:
            # Get student data
            username = str(row['Username']).strip() if pd.notna(row['Username']) else None
            email = str(row['email']).strip().lower() if pd.notna(row['email']) else None
            first_name = str(row['First Name']).strip() if pd.notna(row['First Name']) else ''
            second_name = str(row['Second Name']).strip() if pd.notna(row['Second Name']) else ''
            register_no = str(row['Register number']).strip() if pd.notna(row['Register number']) else ''
            leetcode = str(row['leetcode']).strip() if pd.notna(row['leetcode']) else ''
            mentor_name = row['mentor_filled']
            
            # Skip if no email or username
            if not email or email == 'nan' or not username or username == 'nan':
                skipped_count += 1
                print(f"⚠️  Skipped row {idx+1}: Missing email or username")
                continue
            
            # Use username as-is, but make it unique and lowercase for login
            login_username = username.lower().replace(' ', '_')
            
            # Combine first and second name
            full_name = f"{first_name} {second_name}".strip()
            if not full_name:
                full_name = username
            
            name_parts = full_name.split(' ', 1)
            first = name_parts[0]
            last = name_parts[1] if len(name_parts) > 1 else ''
            
            # Check if user exists
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                user = existing_user
                updated_count += 1
                print(f"⚠️  User exists: {username} ({email})")
            else:
                # Create new user
                user = User.objects.create_user(
                    username=login_username,
                    email=email,
                    password=DEFAULT_PASSWORD,
                    first_name=first,
                    last_name=last,
                )
                created_count += 1
                print(f"✅ Created: {username} ({email}) → Mentor: {mentor_name}")
            
            # Create or update profile
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = 'STUDENT'
            profile.campus = CAMPUS
            profile.floor = FLOOR
            
            # Assign mentor
            if mentor_name in mentor_users:
                profile.assigned_mentor = mentor_users[mentor_name]
            
            profile.save()
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error processing row {idx+1}: {e}")
            continue
    
    # Summary
    print("\n" + "=" * 80)
    print("IMPORT COMPLETE!")
    print("=" * 80)
    print(f"\n✅ Created: {created_count} students")
    print(f"⚠️  Updated: {updated_count} students")
    print(f"⏭️  Skipped: {skipped_count} rows")
    if error_count > 0:
        print(f"❌ Errors: {error_count} rows")
    print(f"\n📊 Total students in database: {User.objects.filter(profile__role='STUDENT').count()}")
    print(f"📊 Total mentors in database: {User.objects.filter(profile__role='MENTOR').count()}")
    print("\n" + "=" * 80)
    print("Login credentials:")
    print("  Students: Use email as username, password: student123")
    print("  Mentors: username format: firstname_lastname, password: mentor123")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    main()
