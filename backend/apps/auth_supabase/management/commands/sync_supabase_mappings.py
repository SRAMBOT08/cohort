"""apps.auth_supabase.management.commands.sync_supabase_mappings

Sync Django users with Supabase Auth users.

Default behavior:
- Fetch existing Supabase Auth users
- Create mappings for Django users that already exist in Supabase

Optional behavior:
- Create missing Supabase Auth users (bulk) and map them

Run:
    python manage.py sync_supabase_mappings
    python manage.py sync_supabase_mappings --create-missing --default-password "pass123@"

Environment:
    SUPABASE_URL
    SUPABASE_SERVICE_ROLE_KEY   (admin access; never expose to frontend)
"""

from __future__ import annotations

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from supabase import create_client

from apps.auth_supabase.models import SupabaseUserMapping


class Command(BaseCommand):
    help = 'Sync Django users with Supabase authentication users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-missing',
            action='store_true',
            help='Create Supabase Auth users for Django users that do not exist in Supabase yet.',
        )
        parser.add_argument(
            '--default-password',
            default=os.getenv('SUPABASE_DEFAULT_PASSWORD', ''),
            help='Password to set for newly created Supabase users (can also set SUPABASE_DEFAULT_PASSWORD).',
        )
        parser.add_argument(
            '--confirm-email',
            action='store_true',
            default=True,
            help='Mark created users as email_confirmed (default: true).',
        )

    def handle(self, *args, **options):
        self.stdout.write('\n🔄 SYNCING USER MAPPINGS')
        self.stdout.write('=' * 80)
        
        # Get Supabase credentials
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        if not url or not key:
            self.stdout.write(self.style.ERROR('❌ Missing Supabase credentials'))
            return
        
        create_missing: bool = bool(options.get('create_missing'))
        default_password: str = (options.get('default_password') or '').strip()
        confirm_email: bool = bool(options.get('confirm_email'))

        if create_missing and not default_password:
            self.stdout.write(self.style.ERROR('❌ --create-missing requires --default-password (or SUPABASE_DEFAULT_PASSWORD)'))
            return

        # Get unmapped users
        unmapped = User.objects.exclude(
            id__in=SupabaseUserMapping.objects.values_list('django_user_id', flat=True)
        ).order_by('email')
        
        total_users = User.objects.count()
        already_mapped = SupabaseUserMapping.objects.count()
        
        self.stdout.write(f'📊 Total Django users: {total_users}')
        self.stdout.write(f'📊 Already mapped: {already_mapped}')
        self.stdout.write(f'📊 Need mapping: {unmapped.count()}\n')
        
        if unmapped.count() == 0:
            self.stdout.write(self.style.SUCCESS('✅ All users already mapped!'))
            return
        
        # Connect to Supabase
        try:
            supabase = create_client(url, key)
            self.stdout.write('📥 Fetching Supabase users...')
            response = supabase.auth.admin.list_users()
            supabase_users = {user.email.lower(): user.id for user in response if getattr(user, 'email', None)}
            self.stdout.write(f'✅ Found {len(supabase_users)} Supabase users\n')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to fetch Supabase users: {e}'))
            return
        
        # Create mappings (and optionally create missing Supabase users)
        created = 0
        created_supabase = 0
        not_found = 0
        skipped_no_email = 0
        errors = 0
        
        self.stdout.write('🔗 Creating mappings...\n')
        
        for i, user in enumerate(unmapped, 1):
            raw_email = (user.email or '').strip()

            # If Django user has no email, we cannot create a Supabase Auth user.
            if not raw_email:
                skipped_no_email += 1
                continue

            email = raw_email.lower()
            
            # Show progress for first 5, every 10th, and last 5
            show_progress = i <= 5 or i % 10 == 0 or i > unmapped.count() - 5
            
            if show_progress:
                self.stdout.write(f'[{i}/{unmapped.count()}] {user.email}')
            
            if email in supabase_users:
                try:
                    SupabaseUserMapping.objects.create(
                        django_user=user,
                        supabase_id=supabase_users[email],
                        supabase_email=email
                    )
                    if show_progress:
                        self.stdout.write(self.style.SUCCESS('   ✅ Created mapping'))
                    created += 1
                except Exception as e:
                    if show_progress:
                        self.stdout.write(self.style.ERROR(f'   ❌ Error: {str(e)[:50]}'))
                    errors += 1
            else:
                if create_missing:
                    try:
                        if show_progress:
                            self.stdout.write('   ➕ Creating Supabase user...')

                        new_user = supabase.auth.admin.create_user({
                            'email': raw_email,
                            'password': default_password,
                            'email_confirm': bool(confirm_email),
                        })

                        supabase_id = new_user.user.id
                        supabase_users[email] = supabase_id
                        created_supabase += 1

                        SupabaseUserMapping.objects.create(
                            django_user=user,
                            supabase_id=supabase_id,
                            supabase_email=email,
                        )
                        created += 1

                        if show_progress:
                            self.stdout.write(self.style.SUCCESS('   ✅ Supabase user + mapping created'))
                    except Exception as e:
                        if show_progress:
                            self.stdout.write(self.style.ERROR(f'   ❌ Failed to create Supabase user: {str(e)[:80]}'))
                        errors += 1
                else:
                    if i <= 5:
                        self.stdout.write(self.style.WARNING('   ⚠️  Not found in Supabase'))
                    not_found += 1
        
        # Summary
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('📊 SYNC SUMMARY')
        self.stdout.write('=' * 80)
        self.stdout.write(self.style.SUCCESS(f'✅ Mappings created: {created}'))
        if create_missing:
            self.stdout.write(self.style.SUCCESS(f'✅ Supabase users created: {created_supabase}'))
        if skipped_no_email > 0:
            self.stdout.write(self.style.WARNING(f'⚠️  Skipped (no email): {skipped_no_email}'))
        self.stdout.write(self.style.WARNING(f'⚠️  Users not in Supabase: {not_found}'))
        if errors > 0:
            self.stdout.write(self.style.ERROR(f'❌ Errors: {errors}'))
        self.stdout.write('=' * 80)
        
        # Final status
        total_mapped = SupabaseUserMapping.objects.count()
        remaining = total_users - total_mapped
        
        self.stdout.write(f'\n📈 FINAL STATUS')
        self.stdout.write(f'   Total users: {total_users}')
        self.stdout.write(f'   Mapped: {total_mapped}')
        self.stdout.write(f'   Remaining: {remaining}')
        
        if remaining == 0:
            self.stdout.write(self.style.SUCCESS('\n🎉 All users are now mapped! Users can login.'))
        else:
            self.stdout.write(self.style.WARNING(f'\n⚠️  {remaining} users still need Supabase accounts'))
