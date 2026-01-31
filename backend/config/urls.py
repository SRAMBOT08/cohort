from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from apps.jwt_serializers import EmailTokenObtainPairSerializer
from apps.users_views import UserProfileView
from apps.setup_view import setup_database
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

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
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
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve React Frontend - catch-all route (must be last)
from django.views.static import serve
from django.http import HttpResponse
import os

def serve_react(request, path=''):
    """Serve React app for all non-API routes"""
    staticfiles_path = os.path.join(settings.BASE_DIR, 'staticfiles')
    
    # If requesting a specific file that exists, serve it
    if path:
        file_path = os.path.join(staticfiles_path, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return serve(request, path, document_root=staticfiles_path)
    
    # For root or non-existent paths, serve index.html
    index_path = os.path.join(staticfiles_path, 'index.html')
    if os.path.exists(index_path):
        return serve(request, 'index.html', document_root=staticfiles_path)
    
    # If index.html doesn't exist, return error
    return HttpResponse(
        f'Frontend not found. index.html should be at: {index_path}<br>'
        f'Staticfiles path: {staticfiles_path}<br>'
        f'Files in staticfiles: {os.listdir(staticfiles_path) if os.path.exists(staticfiles_path) else "Directory not found"}',
        status=503
    )

# Add catch-all route for React frontend (must be last!)
from django.urls import re_path
urlpatterns += [
    re_path(r'^(?!api/|admin/|media/).*$', serve_react),
]
