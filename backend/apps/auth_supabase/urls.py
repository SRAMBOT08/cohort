"""
URL configuration for Supabase auth endpoints
"""
from django.urls import path
from . import views
from .sync_views import sync_mappings_public

app_name = 'auth_supabase'

urlpatterns = [
    # User endpoints
    path('me', views.get_current_user, name='current_user'),
    
    # Protected endpoints
    path('protected', views.protected_view, name='protected'),
    
    # Admin endpoints
    path('admin/stats', views.admin_only_view, name='admin_stats'),
    
    # Sync endpoint (public for initial setup)
    path('sync-mappings/', sync_mappings_public, name='sync_mappings'),
    
    # Health check
    path('health', views.health_check, name='health'),
    path('echo-headers/', views.echo_headers, name='echo_headers'),
    
    # Password Reset (Hybrid Flow)
    # Password Reset (OTP Flow)
    path('password-reset/code/request/', views.request_reset_code, name='request_reset_code'),
    path('password-reset/code/verify/', views.verify_reset_code, name='verify_reset_code'),
]
