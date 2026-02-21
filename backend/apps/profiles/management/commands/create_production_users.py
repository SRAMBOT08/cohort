"""
Management command to create default users for production deployment
Run this on Render after deployment: python manage.py create_production_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile


class Command(BaseCommand):
    help = 'Creates default users for production (admin, student, mentor, floorwing)'

    def handle(self, *args, **options):
        self.stdout.write('Creating production users...\n')
        
        # Create Admin User
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@cohortsummit.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            # Profile is created automatically via signal
            profile = admin.profile
            profile.role = 'ADMIN'
            profile.save()
            self.stdout.write(self.style.SUCCESS('✅ Admin created (username: admin, password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Admin user already exists'))

        # Create Student User
        if not User.objects.filter(username='student').exists():
            student_user = User.objects.create_user(
                username='student',
                email='student@cohortsummit.com',
                password='student123',
                first_name='Test',
                last_name='Student'
            )
            # Profile is created automatically via signal
            profile = student_user.profile
            profile.role = 'STUDENT'
            profile.campus = 'TECH'
            profile.floor = 2
            profile.save()
            self.stdout.write(self.style.SUCCESS('✅ Student created (username: student, password: student123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Student user already exists'))

        # Create Mentor User
        if not User.objects.filter(username='mentor').exists():
            mentor_user = User.objects.create_user(
                username='mentor',
                email='mentor@cohortsummit.com',
                password='mentor123',
                first_name='Test',
                last_name='Mentor'
            )
            # Profile is created automatically via signal
            profile = mentor_user.profile
            profile.role = 'MENTOR'
            profile.campus = 'TECH'
            profile.floor = 2
            profile.save()
            self.stdout.write(self.style.SUCCESS('✅ Mentor created (username: mentor, password: mentor123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Mentor user already exists'))

        # Create Floor Wing User
        if not User.objects.filter(username='floorwing').exists():
            fw_user = User.objects.create_user(
                username='floorwing',
                email='floorwing@cohortsummit.com',
                password='floorwing123',
                first_name='Floor',
                last_name='Wing'
            )
            # Profile is created automatically via signal
            profile = fw_user.profile
            profile.role = 'FLOOR_WING'
            profile.campus = 'TECH'
            profile.floor = 2
            profile.save()
            self.stdout.write(self.style.SUCCESS('✅ Floor Wing created (username: floorwing, password: floorwing123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Floor Wing user already exists'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Production users setup complete!\n'))
        self.stdout.write('Login credentials:')
        self.stdout.write('  Admin:     username=admin,     password=admin123')
        self.stdout.write('  Student:   username=student,   password=student123')
        self.stdout.write('  Mentor:    username=mentor,    password=mentor123')
        self.stdout.write('  FloorWing: username=floorwing, password=floorwing123')
