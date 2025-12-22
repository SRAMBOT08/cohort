"""
Assign all students from dummy users CSV to mentor1
Usage: python assign_csv_students_to_mentor1.py
"""
import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile


def assign_csv_students_to_mentor1():
    """Assign all CSV students to mentor1"""
    
    # Get mentor1
    try:
        mentor = User.objects.get(username='mentor1')
        print(f"✅ Found mentor: {mentor.username} ({mentor.email})")
    except User.DoesNotExist:
        print("❌ mentor1 not found! Please create mentor1 first using create_role_users.py")
        return
    
    # Ensure mentor profile exists
    mentor_profile, _ = UserProfile.objects.get_or_create(user=mentor)
    
    # Read CSV file
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'dummy users - Sheet1.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found at: {csv_path}")
        return
    
    assigned_count = 0
    not_found = []
    
    print(f"\n📊 Processing students from CSV...\n")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row['email'].strip()
            username = row['username'].strip()
            
            # Try to find user by email or username
            try:
                student = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                try:
                    student = User.objects.get(username__iexact=username)
                except User.DoesNotExist:
                    not_found.append(f"{username} ({email})")
                    continue
            
            # Get or create student profile
            student_profile, _ = UserProfile.objects.get_or_create(user=student)
            
            # Assign mentor
            student_profile.assigned_mentor = mentor
            student_profile.save()
            
            assigned_count += 1
            print(f"  ✓ Assigned {student.username} to mentor1")
    
    print(f"\n{'='*60}")
    print(f"✅ Assignment Complete!")
    print(f"{'='*60}")
    print(f"📝 Assigned {assigned_count} students to {mentor.username}")
    
    if not_found:
        print(f"\n⚠️  Students not found in database ({len(not_found)}):")
        for student_info in not_found:
            print(f"  - {student_info}")
        print("\n💡 Tip: Import these students first using import_dummy_users.py")
    
    # Show final summary
    all_assigned = UserProfile.objects.filter(assigned_mentor=mentor).select_related('user')
    print(f"\n👤 Mentor1 now has {all_assigned.count()} total assigned students:")
    for profile in all_assigned:
        print(f"  - {profile.user.username} ({profile.user.email})")


if __name__ == '__main__':
    assign_csv_students_to_mentor1()
