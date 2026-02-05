"""
Django middleware to verify Supabase JWT tokens
"""
import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
import logging

from .models import SupabaseUserMapping
from django.contrib.auth.models import User
from apps.supabase_integration import SupabaseService

logger = logging.getLogger(__name__)


class SupabaseAuthMiddleware:
    """
    Middleware to authenticate requests using Supabase JWT tokens
    
    Flow:
    1. Extract Bearer token from Authorization header
    2. Verify JWT signature using Supabase JWT secret (HS256)
    3. Extract supabase_id from token claims
    4. Map to Django user via SupabaseUserMapping
    5. Attach user to request.user
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip authentication for certain paths
        if self._should_skip_auth(request.path):
            return self.get_response(request)
        
        # Get Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            request.user = AnonymousUser()
            return self.get_response(request)
        
        # Extract token
        token = auth_header.replace('Bearer ', '')
        try:
            token_preview = f"{token[:8]}... (len={len(token)})"
        except Exception:
            token_preview = 'unavailable'
        logger.info(f'Received Authorization token: {token_preview}')
        
        # Verify and decode token
        user, error_type = self._verify_token(token)
        
        if user:
            request.user = user
            request.supabase_token_valid = True
        else:
            # Return 401 for expired/invalid tokens to trigger frontend refresh
            if error_type == 'expired':
                return JsonResponse(
                    {'detail': 'Token expired', 'code': 'token_expired'},
                    status=401
                )
            elif error_type == 'invalid':
                return JsonResponse(
                    {'detail': 'Invalid token', 'code': 'invalid_token'},
                    status=401
                )
            else:
                # For missing or malformed tokens, set anonymous user
                request.user = AnonymousUser()
                request.supabase_token_valid = False
        
        return self.get_response(request)
    
    def _should_skip_auth(self, path):
        """Check if path should skip authentication"""
        skip_paths = [
            '/admin/',
            '/static/',
            '/media/',
            '/api/health/',
        ]
        return any(path.startswith(skip_path) for skip_path in skip_paths)
    
    def _verify_token(self, token):
        """
        Verify Supabase JWT token and return Django user
        Returns: (user, error_type) tuple
        error_type can be: None, 'expired', 'invalid', 'other'
        """
        try:
            # Debug log
            print(f"DEBUG: Starting Supabase token verification... Token len: {len(token)}")
            logger.info("Starting Supabase token verification...")
            
            # Use Supabase admin client to verify token and fetch user
            try:
                client = SupabaseService.get_client()
            except Exception as e:
                print(f"DEBUG: Failed to get Supabase client: {e}")
                logger.error(f"Failed to get Supabase client: {e}")
                return None, 'other'
                
            try:
                response = client.auth.get_user(token)
            except Exception as e:
                print(f"DEBUG: Supabase auth.get_user failed: {e}")
                logger.error(f"Supabase auth.get_user failed: {e}")
                # Check for expiration in the exception message from Supabase/Gotrue
                if 'expired' in str(e).lower():
                    print("DEBUG: Token confirmed expired via exception")
                    return None, 'expired'
                return None, 'invalid'

            supabase_user = getattr(response, 'user', None)
            if not supabase_user:
                print("DEBUG: Supabase returned no user for token")
                logger.warning('Supabase returned no user for token')
                return None, 'invalid'

            supabase_id = getattr(supabase_user, 'id', None)
            if not supabase_id:
                print("DEBUG: Supabase user missing id")
                logger.warning('Supabase user missing id')
                return None, 'invalid'
                
            print(f"DEBUG: Supabase user found: {supabase_id} | {getattr(supabase_user, 'email', 'no-email')}")
            logger.info(f"Supabase user found: {supabase_id} | {getattr(supabase_user, 'email', 'no-email')}")

            # Map to Django user
            django_user = SupabaseUserMapping.get_django_user_by_supabase_id(supabase_id)

            if not django_user:
                print("DEBUG: No existing mapping found. Attempting to create user/mapping...")
                logger.info("No existing mapping found. Attempting to create user/mapping...")
                # Try to find Django user by email and create mapping on-the-fly
                supabase_email = getattr(supabase_user, 'email', None)
                if supabase_email:
                    django_user = User.objects.filter(email=supabase_email).first()

                if not django_user:
                    # Create a new Django user for this Supabase account
                    try:
                        username = (supabase_email.split('@')[0].replace('.', '_')[:150]
                                    if supabase_email else f'user_{supabase_id[:8]}')
                        django_user = User.objects.create_user(
                            username=username,
                            email=supabase_email or '',
                            password=None
                        )
                        print(f"DEBUG: Created Django user: {username}")
                        logger.info(f'Created Django user for Supabase ID: {supabase_id} email: {supabase_email}')
                    except Exception as e:
                        print(f"DEBUG: Failed to create Django user: {e}")
                        logger.error(f'Failed to create Django user: {e}')
                        return None, 'other'

                # Create mapping
                try:
                    SupabaseUserMapping.create_mapping(django_user, supabase_id, supabase_email or '')
                    print(f"DEBUG: Created SupabaseUserMapping for {django_user.username}")
                    logger.info(f'Created SupabaseUserMapping for {django_user.username} <-> {supabase_id}')
                except Exception as e:
                    print(f"DEBUG: Failed to create mapping: {e}")
                    logger.error(f'Failed to create mapping: {e}')
                    # If mapping fails but we have a user, do we fail auth? 
                    # Ideally yes, but for robustness let's return the user anyway if it exists
                    if django_user:
                         print("DEBUG: Mapping failed but returning user anyway.")
                         return django_user, None
                    return None, 'other'
            else:
                print(f"DEBUG: Found existing Django user: {django_user.username} (ID: {django_user.id})")
                logger.info(f"Found existing Django user: {django_user.username} (ID: {django_user.id})")

            # Update last login
            try:
                mapping = django_user.supabase_mapping
                mapping.update_last_login()
            except Exception as e:
                logger.error(f'Failed to update last login: {e}')

            return django_user, None
            
        except jwt.ExpiredSignatureError:
            print("DEBUG: Token expired (jwt)")
            logger.warning('Token expired (jwt)')
            return None, 'expired'
        except jwt.InvalidTokenError as e:
            print(f"DEBUG: Invalid token (jwt): {e}")
            logger.warning(f'Invalid token (jwt): {e}')
            return None, 'invalid'
        except Exception as e:
            print(f"DEBUG: Token verification error: {e}")
            logger.error(f'Token verification error: {e}')
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            # Check if error message indicates expiration
            error_str = str(e).lower()
            if 'expired' in error_str or 'token is expired' in error_str:
                return None, 'expired'
            return None, 'other'
