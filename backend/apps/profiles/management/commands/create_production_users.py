"""
Management command to create default users for production deployment
Run this on Render after deployment: python manage.py create_production_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from apps.profiles.models import UserProfile


class Command(BaseCommand):
    help = 'Creates default users for production (admin, student, mentor, floorwing)'

    def create_or_update_user(self, username, email, password, first_name, last_name, is_superuser=False, role=None, campus='TECH', floor=2):
        """Helper to create or update a user and ensure it's properly configured"""
        created = False
        updated = False
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'Found existing user: {username}')
            
            # Ensure user is active and has correct email
            if not user.is_active:
                user.is_active = True
                updated = True
            if user.email != email:
                user.email = email
                updated = True
            if user.first_name != first_name:
                user.first_name = first_name
                updated = True
            if user.last_name != last_name:
                user.last_name = last_name
                updated = True
            
            # Reset password to ensure it's correct
            user.set_password(password)
            updated = True
            
            if updated:
                user.save()
                self.stdout.write(self.style.WARNING(f'⚠️  Updated existing user: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  User already exists and is configured: {username}'))
                
        except User.DoesNotExist:
            # Create new user
            try:
                if is_superuser:
                    user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )
                created = True
                self.stdout.write(self.style.SUCCESS(f'✅ Created new user: {username}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'❌ Failed to create {username}: {e}'))
                return
        
        # Ensure profile exists and is configured
        if hasattr(user, 'profile'):
            profile = user.profile
        else:
            profile = UserProfile.objects.create(user=user)
            self.stdout.write(f'Created profile for {username}')
        
        if role:
            profile.role = role
            profile.campus = campus
            profile.floor = floor
            profile.save()
        
        return user

    def handle(self, *args, **options):
        from django.db import connection
        
        self.stdout.write('========================================')
        self.stdout.write('Creating/updating production users...')
        self.stdout.write('========================================\n')
        
        # Remove all existing users
        self.stdout.write('🧹 Removing all existing users from database...')
        user_count = User.objects.all().count()
        
        try:
            # First, try to delete any supabase_user_mapping entries if table exists
            with connection.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM supabase_user_mapping")
                    self.stdout.write('✅ Cleared supabase_user_mapping table')
                except Exception as e:
                    self.stdout.write(f'ℹ️  No supabase_user_mapping table to clear: {e}')
            
            # Now delete all users
            User.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'✅ Deleted {user_count} existing users\n'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'⚠️  Could not delete all users: {e}'))
            self.stdout.write(self.style.WARNING('Will update existing users instead\n'))
        
        # Create/Update Admin User
        self.create_or_update_user(
            username='admin',
            email='admin@cohortsummit.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            is_superuser=True,
            role='ADMIN'
        )

        # Create/Update Student User
        self.create_or_update_user(
            username='student',
            email='student@cohortsummit.com',
            password='student123',
            first_name='Test',
            last_name='Student',
            role='STUDENT',
            campus='TECH',
            floor=2
        )

        # Create/Update Mentor User
        self.create_or_update_user(
            username='mentor',
            email='mentor@cohortsummit.com',
            password='mentor123',
            first_name='Test',
            last_name='Mentor',
            role='MENTOR',
            campus='TECH',
            floor=2
        )

        # Create/Update Floor Wing User
        self.create_or_update_user(
            username='floorwing',
            email='floorwing@cohortsummit.com',
            password='floorwing123',
            first_name='Floor',
            last_name='Wing',
            role='FLOOR_WING',
            campus='TECH',
            floor=2
        )

        self.stdout.write('\n========================================')
        self.stdout.write(self.style.SUCCESS('🎉 Production users setup complete!'))
        self.stdout.write('========================================')
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin:     username=admin,     email=admin@cohortsummit.com,     password=admin123')
        self.stdout.write('  Student:   username=student,   email=student@cohortsummit.com,   password=student123')
        self.stdout.write('  Mentor:    username=mentor,    email=mentor@cohortsummit.com,    password=mentor123')
        self.stdout.write('  FloorWing: username=floorwing, email=floorwing@cohortsummit.com, password=floorwing123')
        self.stdout.write('')
