import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.jwt_serializers import EmailTokenObtainPairSerializer
from django.contrib.auth.models import User

try:
    user = User.objects.get(email='jabbastin.k.csd.2024@snsce.ac.in')
    print(f"Found user: {user.username}")
    
    # Simulate serializer usage
    # We need to simulate the data that comes in the request
    data = {
        'username': 'jabbastin.k.csd.2024@snsce.ac.in',
        'password': 'password' # We don't know the password, but we know the validation logic uses authenticate
    }
    
    # We can't easily check password without knowing it, but we can call the logic part that runs AFTER authentication
    # manually if we can't authenticate.
    
    # However, let's try to verify if the "profile data extraction" part works fine.
    
    print("Testing profile data extraction...")
    profile_data = {}
    if hasattr(user, 'profile'):
        print("User has profile")
        profile = user.profile
        profile_data = {
            'role': profile.role,
            'role_display': profile.get_role_display(),
            'campus': profile.campus,
            'campus_display': profile.get_campus_display() if profile.campus else None,
            'floor': profile.floor,
            'floor_display': profile.get_floor_display() if profile.floor else None,
        }
        print("Profile data extracted successfully:", profile_data)
    else:
        print("User has NO profile")

    # Test token generation
    print("Testing token generation...")
    # We need an instance of the serializer
    serializer = EmailTokenObtainPairSerializer()
    try:
        refresh = serializer.get_token(user)
        print("Token generated successfully")
        print("Refresh:", refresh)
        print("Access:", refresh.access_token)
    except Exception as e:
        print(f"Token generation FAILED: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
