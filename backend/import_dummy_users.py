"""
Import dummy student users from CSV file
Run: python import_dummy_users.py
"""
import os
import sys
import django
import csv

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

def import_users():
    """Import users from CSV file"""
    
    # Try multiple possible paths for CSV file
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dummy users - Sheet1.csv'),  # Local dev
        os.path.join(os.path.dirname(__file__), '..', 'dummy users - Sheet1.csv'),  # Relative
        '/opt/render/project/src/dummy users - Sheet1.csv',  # Render absolute
        os.path.join(os.getcwd(), '..', 'dummy users - Sheet1.csv'),  # CWD parent
        os.path.join(os.getcwd(), 'dummy users - Sheet1.csv'),  # CWD
    ]
    
    csv_path = None
    print("Searching for CSV file...")
    for path in possible_paths:
        normalized = os.path.normpath(path)
        print(f"  Checking: {normalized}")
        if os.path.exists(normalized):
            csv_path = normalized
            print(f"  ✓ Found!")
            break
    
    if not csv_path:
        print(f"❌ CSV file not found! Searched paths: {[os.path.normpath(p) for p in possible_paths]}")
        print(f"   Current working directory: {os.getcwd()}")
        return
    
    print(f"\\nReading CSV file: {csv_path}\\n")
    
    created_count = 0
    skipped_count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            email = row['email'].strip()
            username = row['username'].strip()
            password = row['password'].strip()
            
            # Check if user already exists
            user = None
            if User.objects.filter(email=email).exists():
                print(f"🔄 User with email {email} already exists, updating profile...")
                user = User.objects.get(email=email)
            
            if not user:
                # Create username from email if username is same as full name
                # Use email prefix as username to avoid conflicts
                user_username = email.split('@')[0]
                
                # Check if username exists, append number if needed
                base_username = user_username
                counter = 1
                while User.objects.filter(username=user_username).exists():
                    user_username = f"{base_username}{counter}"
                    counter += 1
                
                # Extract first and last name from username
                name_parts = username.split()
                first_name = name_parts[0] if name_parts else username
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                
                # Create user
                user = User.objects.create_user(
                    username=user_username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.set_password(password)
                user.save()
                created_count += 1
                print(f"✅ Created student: {username} ({email}) - username: {user_username}")
            else:
                # Update password for existing user just in case
                user.set_password(password)
                user.save()
                skipped_count += 1
            
            # Update/Fix profile for BOTH new and existing users
            # Use get_or_create to handle missing profiles
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Enforce Student Role
            profile.role = 'STUDENT'
            profile.campus = 'TECH'  # Default campus
            profile.save()
            
            if created:
                print(f"   🐛 Fixed missing profile for {user.username}")
            else:
                print(f"   ✓ Verified profile for {user.username}")
    
    # Print summary
    print("\n" + "="*60)
    print("IMPORT SUMMARY")
    print("="*60)
    print(f"Created: {created_count} users")
    print(f"Skipped: {skipped_count} users (already exist)")
    print("="*60)
    print("\n📝 Default credentials for all users:")
    print("   Password: pass123@")
    print("   Role: STUDENT")
    print("="*60)

if __name__ == '__main__':
    print("Importing dummy student users...\n")
    import_users()
    print("\n✅ Done!")
