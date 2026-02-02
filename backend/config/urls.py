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
from config.health import health_check as render_health_check
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Custom Token View using email authentication
class EmailTokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

# Swagger/OpenAPI Schema
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
)


def serve_frontend_index(request):
    # Serve the React app index.html from staticfiles (after collectstatic)
    import logging
    logger = logging.getLogger(__name__)
    
    index_path = os.path.join(settings.STATIC_ROOT, "frontend", "index.html")
    logger.error(f"🔍 Looking for index.html at: {index_path}")
    logger.error(f"📁 STATIC_ROOT: {settings.STATIC_ROOT}")
    logger.error(f"✅ File exists: {os.path.exists(index_path)}")
    
    if os.path.exists(index_path):
        logger.error(f"✅ Found index.html, serving it")
        with open(index_path, "rb") as f:
            return FileResponse(f, content_type="text/html")
    
    # Fallback for development
    dev_path = os.path.join(settings.BASE_DIR, "static", "frontend", "index.html")
    logger.error(f"🔍 Trying dev path: {dev_path}")
    logger.error(f"✅ Dev file exists: {os.path.exists(dev_path)}")
    
    if os.path.exists(dev_path):
        logger.error(f"✅ Found index.html at dev path, serving it")
        with open(dev_path, "rb") as f:
            return FileResponse(f, content_type="text/html")
    
    # Debug: list what's in staticfiles
    static_root = settings.STATIC_ROOT
    if os.path.exists(static_root):
        try:
            contents = os.listdir(static_root)
            logger.error(f"📂 STATIC_ROOT contents: {contents[:10]}")  # First 10 items
            frontend_path = os.path.join(static_root, "frontend")
            if os.path.exists(frontend_path):
                frontend_contents = os.listdir(frontend_path)
                logger.error(f"📂 frontend/ contents: {frontend_contents}")
        except Exception as e:
            logger.error(f"❌ Error listing directory: {e}")
    
    logger.error(f"❌ Frontend not found anywhere!")
    return HttpResponse(f"Frontend not found. STATIC_ROOT={static_root}, index_path={index_path}", status=500)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Root + SPA fallback (serves built frontend index.html if present)
    path('', serve_frontend_index, name='root_ok'),
    
    # Health Check Endpoints (NEW - for monitoring and scaling)
    path('api/health/', render_health_check, name='render_health_check'),  # Render monitoring
    path('health/', app_health_check, name='health_check'),
    path('health/ready/', readiness_check, name='readiness_check'),
    path('health/live/', liveness_check, name='liveness_check'),
    
    # One-time database setup endpoint
    path('api/setup-database/', setup_database, name='setup_database'),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # JWT Authentication endpoints (with email support)
    path('api/auth/token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile
    path('api/auth/user/', UserProfileView.as_view(), name='user_profile'),
    
    # User Profile Settings
    path('api/profiles/', include('apps.profiles.urls')),
    
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

    # SPA fallback for non-API routes (exclude static files)
    re_path(r'^(?!api/|admin/|static/|assets/).*$', serve_frontend_index, name='spa_fallback'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
