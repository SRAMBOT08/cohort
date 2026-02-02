"""
Django middleware to verify Supabase JWT tokens
"""
import jwt
import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from functools import lru_cache
import logging

from .models import SupabaseUserMapping

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_supabase_jwks():
    """
    Fetch Supabase JSON Web Key Set (JWKS) for JWT verification
    Cached to avoid repeated requests
    """
    try:
        supabase_url = settings.SUPABASE_URL
        jwks_url = f'{supabase_url}/auth/v1/jwks'
        response = requests.get(jwks_url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f'Failed to fetch Supabase JWKS: {e}')
        return None


class SupabaseAuthMiddleware:
    """
    Middleware to authenticate requests using Supabase JWT tokens
    
    Flow:
    1. Extract Bearer token from Authorization header
    2. Verify JWT signature using Supabase public key
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
        
        # Verify and decode token
        user = self._verify_token(token)
        
        if user:
            request.user = user
            request.supabase_token_valid = True
        else:
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
        """
        try:
            # Decode token without verification to get header and kid
            header = jwt.get_unverified_header(token)
            kid = header.get('kid')
            
            # Fetch JWKS (JSON Web Key Set) from Supabase
            jwks = get_supabase_jwks()
            if not jwks:
                logger.error('Failed to fetch JWKS')
                return None
            
            # Find the public key matching the kid
            public_key = None
            for key in jwks.get('keys', []):
                if key.get('kid') == kid:
                    public_key = jwt.algorithms.ECAlgorithm.from_jwk(key)
                    break
            
            if not public_key:
                logger.warning(f'No public key found for kid: {kid}')
                return None
            
            # Verify token with ES256 algorithm
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=['ES256'],
                audience='authenticated',
                options={
                    'verify_signature': True,
                    'verify_exp': True,
                    'verify_aud': True,
                }
            )
            
            # Extract Supabase user ID from token
            supabase_id = decoded.get('sub')
            
            if not supabase_id:
                logger.warning('Token missing sub claim')
                return None
            
            # Map to Django user
            django_user = SupabaseUserMapping.get_django_user_by_supabase_id(supabase_id)
            
            if not django_user:
                logger.warning(f'No Django user found for Supabase ID: {supabase_id}')
                return None
            
            # Update last login
            try:
                mapping = django_user.supabase_mapping
                mapping.update_last_login()
            except Exception as e:
                logger.error(f'Failed to update last login: {e}')
            
            return django_user
            
        except jwt.ExpiredSignatureError:
            logger.warning('Token expired')
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f'Invalid token: {e}')
            return None
        except Exception as e:
            logger.error(f'Token verification error: {e}')
            return None
