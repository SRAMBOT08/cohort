"""
Management command to fix PostgreSQL sequence for auth_user table
Run: python manage.py fix_user_sequence
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix PostgreSQL sequence for auth_user table'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Get the current max ID
            cursor.execute("SELECT MAX(id) FROM auth_user")
            max_id = cursor.fetchone()[0] or 0
            
            # Reset the sequence to max_id + 1
            cursor.execute(f"SELECT setval('auth_user_id_seq', {max_id + 1}, false)")
            new_value = cursor.fetchone()[0]
            
            self.stdout.write(self.style.SUCCESS(
                f'✅ Fixed auth_user sequence. Max ID: {max_id}, Next ID: {new_value}'
            ))
