import os

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from apps.jwt_serializers import EmailTokenObtainPairSerializer
from apps.users_views import UserProfileView
from apps.setup_view import setup_database
from apps.health_check_views import health_check as app_health_check, readiness_check, liveness_check
from apps.debug_views import list_urls
from config.health import health_check as render_health_check
from apps.fix_passwords_view import fix_user_password
from apps.simple_sync_view import simple_sync_mappings
from apps.import_supabase_view import import_from_supabase
from apps.supabase_login_view import supabase_login
from apps.auth_supabase.sync_views import sync_mappings_public
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Custom Token View using email authentication
class EmailTokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

# Swagger/OpenAPI Schema - restrict to specific patterns to avoid 500 errors
schema_view = get_schema_view(
    openapi.Info(
        title="Cohort Web API",
        default_version='v1',
        description="API documentation for Cohort Web Application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@cohort.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    # Restrict to API patterns only to avoid introspection errors
    patterns=[],  # Will generate minimal schema without introspecting all views
)


def serve_frontend_index(request):
    """Frontend is now served from Cloudflare Pages - redirect to API docs"""
    return HttpResponse(
        '{"message": "Cohort Backend API", "status": "running", "docs": "/api/docs/", "frontend": "https://cohort.pages.dev"}',
        content_type="application/json"
    )

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Root - show API info (frontend is on Cloudflare)
    path('', serve_frontend_index, name='root_ok'),
    
    # Health Check Endpoints (NEW - for monitoring and scaling)
    path('api/health/', render_health_check, name='render_health_check'),  # Render monitoring
    path('health/', app_health_check, name='health_check'),
    path('health/ready/', readiness_check, name='readiness_check'),
    path('health/live/', liveness_check, name='liveness_check'),
    # Debug: list loaded URL patterns
    path('api/debug/urls/', list_urls, name='debug_urls'),
    
    # One-time database setup endpoint
    path('api/setup-database/', setup_database, name='setup_database'),
    
    # Fix user password endpoint (temporary for migration)
    path('api/fix-password/', fix_user_password, name='fix_password'),
    
    # Sync Supabase mappings (one-time setup)
    path('api/sync-mappings/', sync_mappings_public, name='sync_mappings'),
    path('api/simple-sync/', simple_sync_mappings, name='simple_sync'),
    path('api/import-from-supabase/', import_from_supabase, name='import_from_supabase'),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # JWT Authentication endpoints (with Supabase)
    path('api/auth/token/', supabase_login, name='token_obtain_pair'),  # Supabase hybrid auth
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile
    path('api/auth/user/', UserProfileView.as_view(), name='user_profile'),
    
    # User Profile Settings
    path('api/profiles/', include('apps.profiles.urls')),
    
    # Supabase Authentication
    path('api/supabase/', include('apps.auth_supabase.urls')),
    
    # App URLs
    path('api/clt/', include('apps.clt.urls')),
    path('api/sri/', include('apps.sri.urls')),
    path('api/cfc/', include('apps.cfc.urls')),
    path('api/iipc/', include('apps.iipc.urls')),
    path('api/scd/', include('apps.scd.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/hackathons/', include('apps.hackathons.urls')),
    
    # Gamification System
    path('api/gamification/', include('apps.gamification.urls')),
    
    # Mentor APIs
    path('api/mentor/', include('apps.mentor_urls')),
    
    # Admin APIs
    path('api/admin/', include('apps.admin_urls')),

    # Removed: SPA fallback - frontend is on Cloudflare Pages
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
