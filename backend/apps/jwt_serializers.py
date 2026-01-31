from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that accepts email or username for authentication
    """
    username_field = 'username'  # This will accept the field name as 'username' but can contain email
    
    def validate(self, attrs):
        try:
            # Get the username field (which might contain email)
            username_or_email = attrs.get('username')
            password = attrs.get('password')
            
            # Try to find user by email first, then by username
            user = None
            try:
                # Check if it's an email
                if '@' in username_or_email:
                    user_obj = User.objects.filter(email=username_or_email).first()
                    if user_obj:
                        user = authenticate(username=user_obj.username, password=password)
                else:
                    user = authenticate(username=username_or_email, password=password)
            except Exception as auth_error:
                # Log authentication error (e.g. DB connection failed)
                import sys
                print(f"LOGIN AUTH ERROR: {str(auth_error)}", file=sys.stderr)
                # If authentication specifically fails due to DB, we might want to re-raise or handle gracefully
                # For now, let's treat it as invalid creds or service unavailable
                pass
            
            if user is None:
                from rest_framework_simplejwt.exceptions import AuthenticationFailed
                raise AuthenticationFailed('No active account found with the given credentials')
            
            # Generate tokens
            refresh = self.get_token(user)
            
            # Get user profile info
            profile_data = {}
            try:
                if hasattr(user, 'profile'):
                    profile = user.profile
                    profile_data = {
                        'role': profile.role,
                        'role_display': profile.get_role_display(),
                        'campus': profile.campus,
                        'campus_display': profile.get_campus_display() if profile.campus else None,
                        'floor': profile.floor,
                        'floor_display': profile.get_floor_display() if profile.floor else None,
                    }
            except Exception as e:
                # Log the error but don't fail the login
                import sys
                print(f"LOGIN PROFILE ERROR: {str(e)}", file=sys.stderr)
                # Default to basic student role if profile fails
                profile_data = {
                    'role': 'STUDENT',
                    'role_display': 'Student',
                    'campus': None,
                    'campus_display': None,
                    'floor': None,
                    'floor_display': None,
                }
            
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'profile': profile_data
                }
            }
            
            return data
            
        except Exception as e:
            # Catch ALL other errors (including DB OperationalError) to prevent 500
            import sys
            print(f"LOGIN CRITICAL ERROR: {str(e)}", file=sys.stderr)
            from rest_framework.exceptions import APIException
            class ServiceUnavailable(APIException):
                status_code = 503
                default_detail = 'Service temporarily unavailable, please try again later.'
                default_code = 'service_unavailable'
            
            # If it's a known auth failure (caught above and re-raised), let it bubble
            if 'No active account' in str(e):
                from rest_framework_simplejwt.exceptions import AuthenticationFailed
                raise AuthenticationFailed('No active account found with the given credentials')
                
            raise ServiceUnavailable(f"Login service error: {str(e)}")
