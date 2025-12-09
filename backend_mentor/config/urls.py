"""
URL Configuration for Mentor Backend

Mentor portal API routes for managing students, reviewing submissions, and communication.
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
        title="Cohort Mentor API",
        default_version='v1',
        description="Mentor portal API for managing assigned students, reviewing submissions, and tracking progress",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="mentor@cohort.local"),
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
    
    # Mentor API endpoints
    path('api/students/', include('apps.student_tracking.urls')),
    path('api/submissions/', include('apps.submission_review.urls')),
    path('api/reports/', include('apps.mentor_reports.urls')),
    path('api/communication/', include('apps.communication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
