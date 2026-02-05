"""
Custom JWT Authentication for Supabase
Handles Supabase JWT tokens and maps to Django users
"""
import jwt
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import User
from .models import SupabaseUserMapping

logger = logging.getLogger(__name__)

class SupabaseJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication for Supabase tokens
    
    This class extends the default JWTAuthentication to:
    1. Verify Supabase JWT tokens using Supabase API (Robust)
    2. Map Supabase user IDs to Django users via SupabaseUserMapping
    3. Handle token validation and user retrieval
    """
    
    def get_validated_token(self, raw_token):
        """
        Validates a JWT token using Supabase User Endpoint (More robust)
        Returns the Supabase User object if valid, raises AuthenticationFailed otherwise.
        """
        try:
            print("DEBUG: [AuthClass] Starting Supabase token verification via API...")
            logger.info("Starting Supabase token verification via API...")
            
            # Use Supabase Service to verify token directly
            from apps.supabase_integration import SupabaseService
            client = SupabaseService.get_client()
            
            # Ensure raw_token is a string (SimpleJWT passes bytes)
            if isinstance(raw_token, bytes):
                raw_token = raw_token.decode('utf-8')
            
            try:
                # Verify token by fetching user
                user_response = client.auth.get_user(raw_token)
                if not user_response or not user_response.user:
                     print("DEBUG: [AuthClass] Token verification returned no user")
                     raise AuthenticationFailed('Token verification returned no user', code='invalid_token')
                
                # Return the user object (as payload substitute)
                print(f"DEBUG: [AuthClass] Token Validated. User ID: {user_response.user.id}")
                return user_response.user
            except Exception as e:
                print(f"DEBUG: [AuthClass] Supabase auth.get_user failed: {e}")
                logger.error(f"Supabase auth.get_user failed: {e}")
                if 'expired' in str(e).lower():
                     raise AuthenticationFailed('Token has expired', code='token_expired')
                raise AuthenticationFailed(f'Invalid token: {e}', code='invalid_token')

        except AuthenticationFailed:
            raise
        except Exception as e:
            print(f"DEBUG: [AuthClass] Token validation error: {e}")
            logger.error(f'Token validation error: {e}')
            raise AuthenticationFailed(f'Token validation failed: {e}', code='token_error')
    
    def get_user(self, validated_token):
        """
        Get Django user from validated Supabase User object
        Maps using SupabaseUserMapping
        """
        try:
            # validated_token is now the Supabase User object from get_validated_token
            supabase_user = validated_token
            supabase_id = getattr(supabase_user, 'id', None)
            
            if not supabase_id:
                raise AuthenticationFailed('Supabase User missing ID')
            
            print(f"DEBUG: [AuthClass] Authenticating Supabase User: {supabase_id}")
            logger.info(f"Authenticated Supabase User: {supabase_id}")

            # Get Django user via mapping
            django_user = SupabaseUserMapping.get_django_user_by_supabase_id(supabase_id)
            
            if not django_user:
                print("DEBUG: [AuthClass] No existing mapping found. Attempting auto-create...")
                # Try to auto-create mapping if we have email in user object
                email = getattr(supabase_user, 'email', None)
                if email:
                    logger.info(f'Attempting auto-mapping for email: {email}')
                    django_user = User.objects.filter(email=email).first()
                    
                    if not django_user:
                        # Auto-create Django user if missing
                        try:
                            username = email.split('@')[0].replace('.', '_')[:150]
                            django_user = User.objects.create_user(
                                username=username,
                                email=email,
                                password=None
                            )
                            print(f"DEBUG: [AuthClass] Created new Django user: {username}")
                            logger.info(f'Created new Django user: {username}')
                        except Exception as e:
                            print(f"DEBUG: [AuthClass] Failed to create Django user: {e}")
                            logger.error(f'Failed to create Django user: {e}')
                            raise AuthenticationFailed('Failed to create user account')

                    if django_user:
                        # Create mapping
                        try:
                            SupabaseUserMapping.objects.get_or_create(
                                django_user=django_user,
                                supabase_id=supabase_id,
                                defaults={'supabase_email': email}
                            )
                            logger.info(f'Created auto-mapping for user {django_user.username}')
                        except Exception as e:
                             print(f"DEBUG: [AuthClass] Failed to create mapping: {e}")
                             logger.error(f"Failed to create mapping: {e}")
                             # Allow proceeding if user exists
                
            if not django_user:
                 print(f"DEBUG: [AuthClass] User not found for Supabase ID: {supabase_id}")
                 logger.warning(f'No Django user found for Supabase ID: {supabase_id}')
                 raise AuthenticationFailed('User not found')
            
            if not django_user.is_active:
                print(f"DEBUG: [AuthClass] User {django_user.username} is inactive")
                raise AuthenticationFailed('User account is disabled')
            
            print(f"DEBUG: [AuthClass] Returning Django User: {django_user.username} (ID: {django_user.id})")
            
            # Update last login
            try:
                if hasattr(django_user, 'supabase_mapping'):
                    django_user.supabase_mapping.update_last_login()
            except Exception:
                pass

            return django_user
            
        except User.DoesNotExist:
            print("DEBUG: [AuthClass] User DoesNotExist")
            raise AuthenticationFailed('User not found')
        except Exception as e:
            print(f"DEBUG: [AuthClass] Error getting user from token: {e}")
            logger.error(f'Error getting user from token: {e}')
            raise AuthenticationFailed('User retrieval failed')
    
    def authenticate(self, request):
        """
        Override authenticate to prevent fallthrough to simplejwt for Supabase tokens.
        If token validation fails and it's clearly a Supabase token (has 'sub' claim),
        don't let it fall through to simplejwt which only accepts HS256.
        """
        try:
            return super().authenticate(request)
        except AuthenticationFailed as e:
            # If we got here, SupabaseJWTAuthentication failed
            # Check if token looks like a Supabase token (has 'sub' claim)
            # If so, don't let it fall through to simplejwt
            auth_header = get_authorization_header(request).split()
            if len(auth_header) == 2:
                try:
                    raw_token = auth_header[1].decode('utf-8')
                    # Decode without verification to check claims
                    unverified = jwt.decode(raw_token, options={"verify_signature": False})
                    if 'sub' in unverified:
                        # This is a Supabase token, don't fall through
                        logger.warning(f'Supabase token validation failed: {e}')
                        raise  # Re-raise the AuthenticationFailed
                except Exception:
                    pass  # Not a valid JWT, let it fall through
            # Not a Supabase token or can't determine, let it fall through to simplejwt
            raise


class AllowAnyJWTAuthentication(SupabaseJWTAuthentication):
    """
    JWT Authentication that doesn't raise exceptions for missing/invalid tokens
    Used for endpoints that should work for both authenticated and anonymous users
    """
    
    def authenticate(self, request):
        """
        Return None instead of raising exception for missing/invalid auth
        This allows the view to fall back to AllowAny permission
        """
        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            # Don't raise exception, just return None to allow anonymous access
            return None
