import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Check admin
admin = User.objects.get(username='admin')
print(f"✅ Admin account ready!")
print(f"   Username: {admin.username}")
print(f"   Email: {admin.email}")
print(f"   Role: {admin.profile.role}")
print(f"   Is Superuser: {admin.is_superuser}")
print(f"   Is Staff: {admin.is_staff}")
