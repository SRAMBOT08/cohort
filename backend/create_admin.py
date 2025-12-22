import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

def create_admin():
    """Create a superuser admin account"""
    
    print("=" * 80)
    print("CREATE ADMIN SUPERUSER")
    print("=" * 80)
    
    # Admin credentials
    email = "admin@cohort.com"
    username = "admin"
    password = "admin123"
    
    # Check if admin already exists
    if User.objects.filter(username=username).exists():
        print(f"⚠️  Admin user '{username}' already exists!")
        
        # Ask if want to delete and recreate
        response = input("Delete and recreate? (y/n): ")
        if response.lower() == 'y':
            User.objects.filter(username=username).delete()
            User.objects.filter(email=email).delete()
            print("🗑️  Deleted existing admin user")
        else:
            print("❌ Cancelled")
            return
    
    # Create superuser
    print(f"\n👤 Creating admin superuser...")
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name="Admin",
        last_name="User"
    )
    
    # Update profile
    profile = user.profile
    profile.role = 'ADMIN'
    profile.save()
    
    print("\n" + "=" * 80)
    print("✅ ADMIN SUPERUSER CREATED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\n📋 Login Credentials:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"\n🔐 Admin Panel: /admin/")
    print(f"🌐 API Access: Full permissions")
    print("\n⚠️  IMPORTANT: Change this password after first login!")
    print("=" * 80)

if __name__ == '__main__':
    create_admin()
