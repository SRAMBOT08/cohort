import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Configuration
CSV_FILE = '../dummy users - Sheet1.csv'
DEFAULT_ROLE = 'STUDENT'

def create_student_from_csv_row(email, username, password):
    """Create a student from CSV row data"""
    try:
        # Check if user already exists by email
        if User.objects.filter(email=email).exists():
            print(f"❌ Email {email} already exists - skipping {username}")
            return None
        
        # Generate unique username from the provided username
        base_username = username.lower().replace(' ', '_')
        unique_username = base_username
        counter = 1
        while User.objects.filter(username=unique_username).exists():
            unique_username = f"{base_username}_{counter}"
            counter += 1
        
        # Split name for first_name and last_name
        name_parts = username.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create user
        user = User.objects.create_user(
            username=unique_username,
            email=email.strip().lower(),
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=False,
            is_superuser=False
        )
        
        # Update profile (created automatically by signal)
        profile = user.profile
        profile.role = DEFAULT_ROLE
        profile.save()
        
        return user, profile
        
    except Exception as e:
        print(f"❌ Error creating student {username}: {e}")
        return None

def main():
    print("=" * 80)
    print("IMPORTING STUDENTS FROM CSV FILE")
    print("=" * 80)
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"❌ CSV file not found: {CSV_FILE}")
        return
    
    # Read CSV file
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            created_count = 0
            skipped_count = 0
            
            print("\nProcessing students...\n")
            
            for row in csv_reader:
                email = row.get('email', '').strip()
                username = row.get('username', '').strip()
                password = row.get('password', '').strip()
                
                if not email or not username or not password:
                    print(f"⚠️  Skipping row with missing data")
                    skipped_count += 1
                    continue
                
                result = create_student_from_csv_row(email, username, password)
                
                if result:
                    user, profile = result
                    print(f"✅ Created: {username} ({email})")
                    created_count += 1
                else:
                    skipped_count += 1
            
            print("\n" + "=" * 80)
            print(f"SUMMARY")
            print("=" * 80)
            print(f"✅ Created: {created_count} students")
            print(f"⚠️  Skipped: {skipped_count} students")
            print("=" * 80)
            
            if created_count > 0:
                print("\n📋 Login Credentials:")
                print("-" * 80)
                
                # Re-read CSV to display credentials
                with open(CSV_FILE, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        email = row.get('email', '').strip()
                        username = row.get('username', '').strip()
                        password = row.get('password', '').strip()
                        if User.objects.filter(email=email.lower()).exists():
                            print(f"User: {username}")
                            print(f"  Email: {email}")
                            print(f"  Password: {password}")
                            print()
            
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return

if __name__ == '__main__':
    main()
