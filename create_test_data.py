#!/usr/bin/env python3
"""Create test data for gamification system"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, '/Users/user/cohort/cohort/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.gamification.models import Season, Episode, Title
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# Ensure test users exist with correct passwords
print("Setting up test users...")
for username, email in [
    ('student', 'student@cohortsummit.com'), 
    ('mentor', 'mentor@cohortsummit.com'), 
    ('floorwing', 'floorwing@cohortsummit.com')
]:
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.set_password('password')
    user.save()
    print(f'✓ User {username} ready')

# Create test season
print("\nCreating test season...")
season, created = Season.objects.get_or_create(
    season_name='Test Season 1',
    defaults={
        'season_number': 1,
        'start_date': timezone.now().date() - timedelta(days=10),
        'end_date': timezone.now().date() + timedelta(days=50),
        'is_active': True,
        'description': 'Test season for endpoint testing'
    }
)
if created:
    print(f'✓ Season created: {season.season_name} (ID: {season.id})')
else:
    print(f'✓ Season exists: {season.season_name} (ID: {season.id})')

# Create test episodes
print("\nCreating test episodes...")
for i in range(1, 4):
    episode, created = Episode.objects.get_or_create(
        season=season,
        episode_number=i,
        defaults={
            'title': f'Episode {i}',
            'description': f'Test episode {i}',
            'release_date': timezone.now().date() - timedelta(days=10-i),
            'due_date': timezone.now().date() + timedelta(days=i*10),
        }
    )
    if created:
        print(f'✓ Episode created: {episode.title} (ID: {episode.id})')
    else:
        print(f'✓ Episode exists: {episode.title} (ID: {episode.id})')

# Create test titles
print("\nCreating test titles...")
for i, title_name in enumerate(['Novice', 'Apprentice', 'Expert'], 1):
    title, created = Title.objects.get_or_create(
        title_name=title_name,
        defaults={
            'description': f'{title_name} level title',
            'threshold_points': i * 100,
            'icon': f'icon_{title_name.lower()}.png'
        }
    )
    if created:
        print(f'✓ Title created: {title.title_name}')
    else:
        print(f'✓ Title exists: {title.title_name}')

print('\n✅ Test data setup completed successfully!')
