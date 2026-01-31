"""
Test database connection and auth endpoint
Run on Render: python test_database_connection.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile
from django.db import connection

def test_database_connection():
    """Test if database is accessible"""
    
    print(f"\n{'='*60}")
    print(f"Testing Database Connection")
    print(f"{'='*60}\n")
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✓ Database connection successful: {result}")
        
        # Test if tables exist
        print(f"\n✓ Testing table access...")
        user_count = User.objects.count()
        print(f"  - Users table: {user_count} users")
        
        profile_count = UserProfile.objects.count()
        print(f"  - UserProfile table: {profile_count} profiles")
        
        # Test a specific user
        print(f"\n✓ Testing user retrieval...")
        try:
            student = User.objects.filter(email='student@cohort.com').first()
            if student:
                print(f"  - Found student@cohort.com: {student.username}")
                print(f"  - Has profile: {hasattr(student, 'profile')}")
                if hasattr(student, 'profile'):
                    print(f"  - Profile role: {student.profile.role}")
            else:
                print(f"  ⚠️  student@cohort.com not found")
        except Exception as e:
            print(f"  ❌ Error retrieving student: {e}")
        
        print(f"\n{'='*60}")
        print(f"Database Status: OK")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection failed!")
        print(f"Error: {e}")
        print(f"\nDatabase settings:")
        print(f"  - DATABASE_URL: {'Set' if os.getenv('DATABASE_URL') else 'Not set'}")
        print(f"  - DB_ENGINE: {os.getenv('DB_ENGINE', 'Not set')}")
        print(f"\n{'='*60}\n")
        return False


def test_authentication():
    """Test JWT authentication"""
    
    print(f"\n{'='*60}")
    print(f"Testing Authentication")
    print(f"{'='*60}\n")
    
    try:
        from django.contrib.auth import authenticate
        from apps.jwt_serializers import EmailTokenObtainPairSerializer
        
        # Test authentication with student@cohort.com
        test_email = 'student@cohort.com'
        test_password = 'pass123#'
        
        print(f"Attempting to authenticate: {test_email}")
        
        # Find user by email
        user = User.objects.filter(email=test_email).first()
        if not user:
            print(f"❌ User not found: {test_email}")
            return False
        
        print(f"✓ User found: {user.username}")
        
        # Test password
        if user.check_password(test_password):
            print(f"✓ Password is correct")
        else:
            print(f"❌ Password is incorrect")
            return False
        
        # Test authenticate function
        auth_user = authenticate(username=user.username, password=test_password)
        if auth_user:
            print(f"✓ Django authenticate() successful")
        else:
            print(f"❌ Django authenticate() failed")
            return False
        
        # Test JWT serializer
        print(f"\n✓ Testing JWT token generation...")
        serializer = EmailTokenObtainPairSerializer(data={
            'username': test_email,
            'password': test_password
        })
        
        if serializer.is_valid():
            tokens = serializer.validated_data
            print(f"✓ JWT tokens generated successfully")
            print(f"  - Access token length: {len(tokens.get('access', ''))}")
            print(f"  - Refresh token length: {len(tokens.get('refresh', ''))}")
        else:
            print(f"❌ JWT serializer validation failed")
            print(f"  Errors: {serializer.errors}")
            return False
        
        print(f"\n{'='*60}")
        print(f"Authentication Status: OK")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Authentication test failed!")
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n{'='*60}\n")
        return False


if __name__ == '__main__':
    db_ok = test_database_connection()
    
    if db_ok:
        auth_ok = test_authentication()
        
        if db_ok and auth_ok:
            print(f"\n✅ ALL TESTS PASSED")
            sys.exit(0)
        else:
            print(f"\n❌ SOME TESTS FAILED")
            sys.exit(1)
    else:
        print(f"\n❌ DATABASE CONNECTION FAILED")
        sys.exit(1)
