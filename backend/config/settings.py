import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-change-this')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# In development, allow all hosts to avoid DisallowedHost during local testing
if os.getenv('FORCE_ALLOW_ALL_HOSTS', None) == '1' or os.getenv('DJANGO_ALLOW_ALL_HOSTS', None) == '1' or (os.getenv('ENV', '').lower() != 'production' and os.getenv('DEBUG', 'True') == 'True'):
    ALLOWED_HOSTS = ['*']

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    # Removed: 'rest_framework_simplejwt' - Using Supabase-only authentication
    'corsheaders',
    'drf_yasg',
    
    # Local apps (5 main modules)
    'apps.clt',
    'apps.sri',
    'apps.cfc',
    'apps.iipc',
    'apps.scd',
    'apps.profiles',
    'apps.dashboard',
    'hackathons',
    
    # Gamification System
    'apps.gamification',
    
    # Analytics & Scaling (NEW - for 2000+ students)
    'apps.analytics_summary',
    
    # Supabase Authentication
    'apps.auth_supabase',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'corsheaders.middleware.CorsMiddleware',  # CORS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'apps.auth_supabase.middleware.SupabaseAuthMiddleware',  # DISABLED: Using DRF Auth Class instead
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ...

# Django REST Framework Settings
# Using Supabase-only authentication via SupabaseAuthMiddleware
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.auth_supabase.authentication.SupabaseJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT Settings (handled by auth team)
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_LIFETIME_DAYS', 7))),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': os.getenv('JWT_ALGORITHM', 'HS256'),
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),
}

# Swagger/OpenAPI Settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
}

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# ============================================================================
# SCALING FEATURE FLAGS (LOCAL SAFE, CLOUD READY)
# ============================================================================
# These flags enable performance optimizations without breaking existing code.
# All flags default to False/Local to keep development simple.

# Analytics Optimization
USE_ANALYTICS_SUMMARY = os.getenv('USE_ANALYTICS_SUMMARY', 'False') == 'True'
# When True: Uses pre-computed analytics summaries (fast, scales to 2000+ students)
# When False: Uses live aggregation (current behavior, development mode)

# Notification Optimization
USE_NOTIFICATION_CACHE = os.getenv('USE_NOTIFICATION_CACHE', 'False') == 'True'
# When True: Caches notification counts for 30 seconds
# When False: Always computes counts live (current behavior)

# File Storage
USE_CLOUD_STORAGE = os.getenv('USE_CLOUD_STORAGE', 'False') == 'True'
# When True: Uses AWS S3 or cloud storage (production)
# When False: Uses local filesystem (current behavior, development)

# Background Tasks
USE_ASYNC_TASKS = os.getenv('USE_ASYNC_TASKS', 'False') == 'True'
# When True: Uses Celery/Redis for background tasks (production)
# When False: Tasks run synchronously (current behavior, development)

# Database Query Logging (Debug only)
LOG_QUERY_TIMES = DEBUG and os.getenv('LOG_QUERY_TIMES', 'False') == 'True'
# When True: Logs slow queries to console (helpful for optimization)
# When False: No query logging (default)

# ============================================================================
# CACHING CONFIGURATION (LOCAL SAFE, REDIS READY)
# ============================================================================
if USE_NOTIFICATION_CACHE or USE_ANALYTICS_SUMMARY:
    # Use Redis if available in production, otherwise local memory cache
    REDIS_URL = os.getenv('REDIS_URL', None)
    if REDIS_URL and not DEBUG:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                'LOCATION': REDIS_URL,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                },
                'KEY_PREFIX': 'cohort',
                'TIMEOUT': 300,  # 5 minutes default
            }
        }
    else:
        # Local development: Use in-memory cache (no Redis required)
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'cohort-cache',
                'TIMEOUT': 300,
            }
        }
else:
    # No caching (current behavior)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# ============================================================================
# AWS/CLOUD STORAGE CONFIGURATION (OPTIONAL)
# ============================================================================
if USE_CLOUD_STORAGE:
    # TODO: Add django-storages and boto3 to requirements.txt when needed
    # pip install django-storages boto3
    # 
    # INSTALLED_APPS += ['storages']
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    # AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    # AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    # AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    # AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    # AWS_S3_FILE_OVERWRITE = False
    # AWS_DEFAULT_ACL = None
    # AWS_S3_OBJECT_PARAMETERS = {
    #     'CacheControl': 'max-age=86400',
    # }
    pass

# ============================================================================
# CELERY CONFIGURATION (PLACEHOLDER FOR FUTURE)
# ============================================================================
if USE_ASYNC_TASKS:
    # TODO: Add celery and redis to requirements.txt when needed
    # pip install celery redis
    #
    # CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    # CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    # CELERY_ACCEPT_CONTENT = ['json']
    # CELERY_TASK_SERIALIZER = 'json'
    # CELERY_RESULT_SERIALIZER = 'json'
    # CELERY_TIMEZONE = TIME_ZONE
    # CELERY_TASK_TRACK_STARTED = True
    # CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
    pass
