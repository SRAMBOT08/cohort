"""
Example API views using Supabase authentication
"""
import json
import logging
import requests
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .decorators import supabase_auth_required, supabase_admin_required
from .models import PasswordResetCode, SupabaseUserMapping
import random
import uuid
from django.utils import timezone
from supabase import create_client

@require_http_methods(['POST'])
@csrf_exempt
def request_reset_code(request):
    """
    POST /api/supabase/password-reset/code/request/
    Generates a 6-digit code and emails it.
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
            
        email = email.lower().strip()
        
        # 1. Generate Code
        code = str(random.randint(100000, 999999))
        
        # 2. Save Code to DB
        PasswordResetCode.objects.create(email=email, code=code)
        
        # 3. Send Email
        subject = f"Your Password Reset Code: {code}"
        message = f"Here is your secure verification code to reset your password:\n\n{code}\n\nThis code expires in 15 minutes.\nDo not share this code with anyone."
        
        # Use our Unverified Backend if configured in settings, otherwise standard
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return JsonResponse({'message': 'Verification code sent to email.'})
        
    except Exception as e:
        logger.error(f"Request Code Error: {str(e)}")
        return JsonResponse({'error': f'Failed to send code: {str(e)}'}, status=500)


@require_http_methods(['POST'])
@csrf_exempt
def verify_reset_code(request):
    """
    POST /api/supabase/password-reset/code/verify/
    Verify code and update password.
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('new_password')
        
        if not all([email, code, new_password]):
            return JsonResponse({'error': 'Email, code, and new password are required'}, status=400)
            
        email = email.lower().strip()
        
        # 1. Find Valid Code
        # We get the latest code for this email that is NOT used
        reset_obj = PasswordResetCode.objects.filter(email=email, code=code, used=False).order_by('-created_at').first()
        
        if not reset_obj:
            return JsonResponse({'error': 'Invalid code.'}, status=400)
            
        # 2. Check Expiry/Attempts
        if not reset_obj.is_valid():
             return JsonResponse({'error': 'Code expired or invalid.'}, status=400)
             
        # 3. Update Password in Supabase
        supabase_url = settings.SUPABASE_URL
        supabase_key = settings.SUPABASE_SERVICE_ROLE_KEY
        
        # Initialize Supabase Client (Admin)
        supabase = create_client(supabase_url, supabase_key)
        
        # Strategy: Use `SupabaseUserMapping` first.
        mapping = SupabaseUserMapping.objects.filter(supabase_email=email).first()
        user_id = mapping.supabase_id if mapping else None
        
        if not user_id:
            return JsonResponse({'error': 'User not found in system records. Please contact support.'}, status=404)
        
        # 4. Update Password
        # Using raw request to ensure compatibility
        admin_url = f"{supabase_url}/auth/v1/admin/users/{user_id}"
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        res = requests.put(admin_url, headers=headers, json={"password": new_password})
        
        if res.status_code != 200:
            return JsonResponse({'error': f'Supabase Error: {res.text}'}, status=400)
            
        # 5. Mark Code as Used
        reset_obj.used = True
        reset_obj.save()
        
        return JsonResponse({'message': 'Password updated successfully.'})
        
    except Exception as e:
        logger.error(f"Verify Error: {str(e)}")
        return JsonResponse({'error': f'Failed to update password: {str(e)}'}, status=500)


@require_http_methods(['GET'])
@supabase_auth_required
def get_current_user(request):
    """
    GET /api/me
    Returns current authenticated user info
    """
    user = request.user
    
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined.isoformat(),
    })


@require_http_methods(['GET'])
@supabase_auth_required
def protected_view(request):
    """
    GET /api/protected
    Example of a protected endpoint
    """
    return JsonResponse({
        'message': 'This is protected data',
        'user': request.user.username,
        'access_granted': True,
    })


@require_http_methods(['GET'])
@supabase_admin_required
def admin_only_view(request):
    """
    GET /api/admin/stats
    Example of an admin-only endpoint
    """
    return JsonResponse({
        'message': 'Admin access granted',
        'admin': request.user.username,
        'stats': {
            'total_users': 100,
            'active_sessions': 25,
        }
    })


@require_http_methods(['GET'])
def health_check(request):
    """
    GET /api/health
    Public health check endpoint
    """
    return JsonResponse({
        'status': 'ok',
        'service': 'django-supabase-auth'
    })


@require_http_methods(['GET'])
def echo_headers(request):
    """
    Debug endpoint to echo incoming Authorization header (safe preview).
    GET /api/supabase/echo-headers/
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    try:
        preview = f"{auth_header[:40]}... (len={len(auth_header)})" if auth_header else ''
    except Exception:
        preview = 'unavailable'

    return JsonResponse({
        'authorization_header_present': bool(auth_header),
        'authorization_preview': preview,
    })
