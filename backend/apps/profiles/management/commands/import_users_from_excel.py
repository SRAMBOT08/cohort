"""
Management command to import users from Excel file (package-lock.xlsx)
Automatically runs during build process on Render
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile
import os


class Command(BaseCommand):
    help = 'Import users from package-lock.xlsx file'

    def handle(self, *args, **options):
        try:
            import pandas as pd
        except ImportError:
            self.stdout.write(self.style.ERROR('❌ pandas not installed. Install with: pip install pandas openpyxl'))
            return
        
        self.stdout.write('========================================')
        self.stdout.write('📋 Importing users from Excel file')
        self.stdout.write('========================================\n')
        
        # Excel file path
        excel_file = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'package-lock.xlsx')
        
        if not os.path.exists(excel_file):
            self.stdout.write(self.style.WARNING(f'⚠️  Excel file not found at: {excel_file}'))
            self.stdout.write(self.style.WARNING('Skipping user import from Excel'))
            return
        
        self.stdout.write(f'📄 Reading Excel file: package-lock.xlsx\n')
        
        try:
            # Read Excel file - try different header configurations
            df = pd.read_excel(excel_file)
            
            # Display file info
            self.stdout.write(f'Total rows: {len(df)}')
            self.stdout.write(f'Columns found: {list(df.columns)}\n')
            
            # Clean up - remove empty rows
            df = df.dropna(how='all')
            
            # Detect column names (flexible matching)
            username_col = self._find_column(df, ['username', 'user name', 'user', 'login'])
            email_col = self._find_column(df, ['email', 'mail', 'e-mail', 'mail id'])
            roll_col = self._find_column(df, ['roll', 'roll no', 'roll number', 'register no', 'registration', 'reg no'])
            name_col = self._find_column(df, ['name', 'student name', 'full name'])
            mentor_col = self._find_column(df, ['mentor', 'mentor name', 'assigned mentor'])
            
            if not email_col:
                self.stdout.write(self.style.ERROR('❌ Could not find email column in Excel file'))
                return
            
            # Process each row
            created_count = 0
            updated_count = 0
            error_count = 0
            mentor_cache = {}
            
            for idx, row in df.iterrows():
                try:
                    email = str(row[email_col]).strip().lower() if pd.notna(row[email_col]) else None
                    
                    if not email or email == 'nan' or '@' not in email:
                        continue
                    
                    # Extract data
                    username = self._get_value(row, username_col, f'user_{idx+1}')
                    roll_no = self._get_value(row, roll_col, '')
                    name = self._get_value(row, name_col, username)
                    mentor_name = self._get_value(row, mentor_col, None)
                    
                    # Parse name
                    name_parts = str(name).split(' ', 1)
                    first_name = name_parts[0]
                    last_name = name_parts[1] if len(name_parts) > 1 else ''
                    
                    # Create or update user
                    user, created = User.objects.get_or_create(
                        email=email,
                        defaults={
                            'username': username,
                            'first_name': first_name,
                            'last_name': last_name,
                        }
                    )
                    
                    if created:
                        # Set default password
                        user.set_password('student123')
                        user.save()
                        created_count += 1
                        self.stdout.write(f'✅ Created user: {username} ({email})')
                    else:
                        updated_count += 1
                        self.stdout.write(f'⚠️  User exists: {username} ({email})')
                    
                    # Create or update profile
                    profile, _ = UserProfile.objects.get_or_create(user=user)
                    profile.role = 'STUDENT'
                    profile.campus = 'TECH'
                    profile.floor = 2
                    
                    # Assign mentor if specified
                    if mentor_name and mentor_name != 'nan':
                        mentor_user = self._find_or_cache_mentor(mentor_name, mentor_cache)
                        if mentor_user:
                            profile.assigned_mentor = mentor_user
                            self.stdout.write(f'   👤 Assigned mentor: {mentor_name}')
                    
                    profile.save()
                    
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'❌ Error processing row {idx+1}: {e}'))
            
            # Summary
            self.stdout.write('\n========================================')
            self.stdout.write(self.style.SUCCESS(f'✅ Import Complete!'))
            self.stdout.write(f'   Created: {created_count} users')
            self.stdout.write(f'   Updated: {updated_count} users')
            if error_count > 0:
                self.stdout.write(self.style.WARNING(f'   Errors: {error_count} rows'))
            self.stdout.write('========================================\n')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to read Excel file: {e}'))
            self.stdout.write(self.style.ERROR(f'Error details: {type(e).__name__}'))
    
    def _find_column(self, df, possible_names):
        """Find column by matching possible names (case-insensitive)"""
        columns_lower = {col.lower(): col for col in df.columns}
        for name in possible_names:
            if name.lower() in columns_lower:
                return columns_lower[name.lower()]
        return None
    
    def _get_value(self, row, column, default=''):
        """Safely get value from row"""
        if not column or column not in row:
            return default
        value = row[column]
        if pd.isna(value) or str(value).strip() == '' or str(value) == 'nan':
            return default
        return str(value).strip()
    
    def _find_or_cache_mentor(self, mentor_name, cache):
        """Find mentor by name and cache the result"""
        if mentor_name in cache:
            return cache[mentor_name]
        
        # Try to find mentor by name
        mentor_profile = UserProfile.objects.filter(
            role='MENTOR',
            user__first_name__icontains=mentor_name.split()[0]
        ).first()
        
        if not mentor_profile:
            # Try to find by username or email
            mentor_profile = UserProfile.objects.filter(
                role='MENTOR',
                user__username__icontains=mentor_name.lower().replace(' ', '')
            ).first()
        
        mentor_user = mentor_profile.user if mentor_profile else None
        cache[mentor_name] = mentor_user
        return mentor_user
