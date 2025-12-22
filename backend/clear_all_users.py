import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

def clear_all_users():
    """Clear all users and profiles from the database"""
    
    print("=" * 80)
    print("CLEARING ALL USERS FROM DATABASE")
    print("=" * 80)
    
    # Count before deletion
    user_count = User.objects.count()
    profile_count = UserProfile.objects.count()
    
    print(f"\n📊 Current database state:")
    print(f"   Users: {user_count}")
    print(f"   Profiles: {profile_count}")
    
    if user_count == 0:
        print("\n✅ Database is already empty!")
        return
    
    # Delete all profiles first (although cascade should handle this)
    print(f"\n🗑️  Deleting {profile_count} profiles...")
    UserProfile.objects.all().delete()
    
    # Delete all users
    print(f"🗑️  Deleting {user_count} users...")
    User.objects.all().delete()
    
    # Verify deletion
    remaining_users = User.objects.count()
    remaining_profiles = UserProfile.objects.count()
    
    print("\n" + "=" * 80)
    print("DELETION COMPLETE")
    print("=" * 80)
    print(f"✅ Deleted {user_count} users")
    print(f"✅ Deleted {profile_count} profiles")
    print(f"\n📊 Remaining in database:")
    print(f"   Users: {remaining_users}")
    print(f"   Profiles: {remaining_profiles}")
    print("=" * 80)
    print("\n🎉 Database is now clean and ready for fresh deployment!")

if __name__ == '__main__':
    clear_all_users()
