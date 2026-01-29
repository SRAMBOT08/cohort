#!/usr/bin/env python
"""
Create/Reset admin user for the Cohort platform
Works with both custom User models (email-based) and Django's default User model
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Admin credentials - try both .edu and .com domains
emails_to_try = ['admin@cohort.edu', 'admin@cohort.com']
password = 'admin123'
username = 'admin'

def create_or_update_admin():
    """Create or update admin user"""
    
    # Check if we're using a custom user model or Django's default
    uses_username = hasattr(User, 'USERNAME_FIELD') and User.USERNAME_FIELD == 'username'
    
    admin_user = None
    
    # Try to find existing admin user by email
    for email in emails_to_try:
        if hasattr(User.objects, 'filter'):
            admin_user = User.objects.filter(email=email).first()
            if admin_user:
                print(f'✅ Found existing admin user with email: {email}')
                break
    
    # Try to find by username if not found by email
    if not admin_user and uses_username:
        admin_user = User.objects.filter(username=username).first()
        if admin_user:
            print(f'✅ Found existing admin user with username: {username}')
    
    if admin_user:
        print('🔄 Updating existing admin user...')
        admin_user.set_password(password)
        admin_user.is_active = True
        admin_user.is_staff = True
        admin_user.is_superuser = True
        
        # Set role if the model has it (custom user model)
        if hasattr(admin_user, 'role'):
            admin_user.role = 'ADMIN'
        
        # Update username if needed
        if uses_username:
            admin_user.username = username
            
        admin_user.save()
        
        # Update profile if it exists
        if hasattr(admin_user, 'profile'):
            profile = admin_user.profile
            if hasattr(profile, 'role'):
                profile.role = 'ADMIN'
                profile.save()
                
        print('✅ Admin user updated successfully!')
        final_email = admin_user.email
        
    else:
        print('🆕 Creating new admin user...')
        
        # Use the first email in the list
        email = emails_to_try[0]
        
        try:
            if uses_username:
                # Django's default User model
                admin_user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
            else:
                # Custom User model (email-based)
                admin_user = User.objects.create_superuser(
                    email=email,
                    password=password
                )
            
            # Set role if the model has it
            if hasattr(admin_user, 'role'):
                admin_user.role = 'ADMIN'
                admin_user.save()
            
            # Update profile if it exists
            if hasattr(admin_user, 'profile'):
                profile = admin_user.profile
                if hasattr(profile, 'role'):
                    profile.role = 'ADMIN'
                    profile.save()
                    
            print('✅ Admin user created successfully!')
            final_email = email
            
        except Exception as e:
            print(f'❌ Error creating admin user: {e}')
            return
    
    # Print credentials
    print(f'\n{"="*60}')
    print('🔑 ADMIN LOGIN CREDENTIALS:')
    print(f'{"="*60}')
    if uses_username:
        print(f'Username: {username}')
    print(f'Email: {final_email}')
    print(f'Password: {password}')
    print(f'{"="*60}')
    print('\n✨ You can now log in to the admin panel!')
    print(f'{"="*60}\n')

if __name__ == '__main__':
    create_or_update_admin()
