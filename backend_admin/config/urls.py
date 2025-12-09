"""
URL Configuration for Admin Backend

Admin portal API routes for managing the entire cohort system.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Cohort Admin API",
        default_version='v1',
        description="Admin portal API for managing cohort system - users, mentors, students, analytics, and system configuration",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="admin@cohort.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Admin API endpoints
    path('api/users/', include('apps.user_management.urls')),
    path('api/mentors/', include('apps.mentor_management.urls')),
    path('api/cohorts/', include('apps.cohort_management.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
