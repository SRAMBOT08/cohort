"""
Management command to check and display production user status
Run: python manage.py check_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Check status of production users'

    def handle(self, *args, **options):
        self.stdout.write('=== Production Users Status ===\n')
        
        usernames = ['admin', 'student', 'mentor', 'floorwing']
        
        for username in usernames:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(f'\n✅ {username.upper()}:')
                self.stdout.write(f'   ID: {user.id}')
                self.stdout.write(f'   Email: {user.email}')
                self.stdout.write(f'   Is Active: {user.is_active}')
                self.stdout.write(f'   Is Staff: {user.is_staff}')
                self.stdout.write(f'   Is Superuser: {user.is_superuser}')
                
                if hasattr(user, 'profile'):
                    self.stdout.write(f'   Profile Role: {user.profile.role}')
                    self.stdout.write(f'   Profile Campus: {user.profile.campus}')
                else:
                    self.stdout.write(self.style.WARNING('   ⚠️  No profile found'))
                    
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'\n❌ {username.upper()}: NOT FOUND'))
        
        self.stdout.write('\n\n=== Database Info ===')
        # Check sequence
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT last_value FROM auth_user_id_seq")
            seq_value = cursor.fetchone()[0]
            cursor.execute("SELECT MAX(id) FROM auth_user")
            max_id = cursor.fetchone()[0] or 0
            
            self.stdout.write(f'Max User ID: {max_id}')
            self.stdout.write(f'Sequence Value: {seq_value}')
            
            if seq_value <= max_id:
                self.stdout.write(self.style.WARNING('⚠️  Sequence is behind! Run: python manage.py fix_user_sequence'))
            else:
                self.stdout.write(self.style.SUCCESS('✅ Sequence is OK'))
