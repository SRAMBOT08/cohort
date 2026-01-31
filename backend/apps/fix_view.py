from django.http import JsonResponse
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile
import csv
import os

def fix_users_view(request):
    """
    Temporary endpoint to fix user profiles from CSV.
    Accessible via GET request for ease of use.
    """
    results = {
        'status': 'started',
        'fixed': [],
        'created': [], 
        'verified': [],
        'errors': [],
        'csv_path_used': None
    }
    
    # Logic to find CSV
    # We look in likely locations relative to this file and the app root
    current_dir = os.path.dirname(__file__)
    backend_dir = os.path.dirname(current_dir)
    root_dir = os.path.dirname(backend_dir)
    
    possible_paths = [
        os.path.join(root_dir, 'dummy users - Sheet1.csv'), # Local dev root
        os.path.join(backend_dir, 'dummy users - Sheet1.csv'), # Backend root
        '/app/dummy users - Sheet1.csv', # Render root
        '/app/backend/dummy users - Sheet1.csv', # Render backend
        '/opt/render/project/src/dummy users - Sheet1.csv', # Another Render path
        'dummy users - Sheet1.csv', # CWD
    ]
    
    csv_path = None
    checked_paths = []
    for path in possible_paths:
        normalized = os.path.normpath(path)
        checked_paths.append(normalized)
        if os.path.exists(normalized):
            csv_path = normalized
            break
            
    if not csv_path:
        return JsonResponse({
            'error': 'CSV file not found', 
            'searched_paths': checked_paths,
            'current_working_directory': os.getcwd()
        }, status=404)
        
    results['csv_path_used'] = csv_path
        
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    email = row.get('email', '').strip()
                    if not email:
                        continue
                        
                    username = row.get('username', '').strip()
                    password = row.get('password', '').strip()
                    
                    # 1. Ensure User Exists
                    user = None
                    if User.objects.filter(email=email).exists():
                        user = User.objects.get(email=email)
                        # Optional: Update password
                        # user.set_password(password)
                        # user.save()
                    else:
                        # Create new
                        user_username = email.split('@')[0]
                        # Handling duplicate usernames simple logic
                        if User.objects.filter(username=user_username).exists():
                            user_username = f"{user_username}_new"
                            
                        user = User.objects.create_user(
                            username=user_username,
                            email=email,
                            password=password,
                            first_name=username.split()[0] if username else '',
                        )
                        results['created'].append(email)
                    
                    # 2. Fix Profile
                    profile, created = UserProfile.objects.get_or_create(user=user)
                    
                    # Update fields if needed
                    updates_made = False
                    if profile.role != 'STUDENT':
                        profile.role = 'STUDENT'
                        updates_made = True
                    if profile.campus != 'TECH':
                        profile.campus = 'TECH'
                        updates_made = True
                        
                    if updates_made or created:
                        profile.save()
                        results['fixed'].append(email)
                    else:
                        results['verified'].append(email)
                        
                except Exception as row_error:
                    results['errors'].append(f"Row error ({email}): {str(row_error)}")
                    
    except Exception as e:
        results['errors'].append(f"File error: {str(e)}")
        
    results['status'] = 'completed'
    return JsonResponse(results)
