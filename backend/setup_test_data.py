import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.gamification.models import Season, Episode, Title
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# Setup users
for username, email in [('student', 'student@cohortsummit.com'), ('mentor', 'mentor@cohortsummit.com'), ('floorwing', 'floorwing@cohortsummit.com')]:
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.set_password('password')
    user.save()
    print(f'User {username} ready')

# Create season
season, created = Season.objects.get_or_create(
    season_number=1,
    defaults={
        'name': 'Test Season 1',
        'start_date': timezone.now().date() - timedelta(days=10),
        'end_date': timezone.now().date() + timedelta(days=50),
        'is_active': True,
    }
)
print(f'Season: {season.name} (ID: {season.id})')

# Create episodes
for i in range(1, 4):
    episode, created = Episode.objects.get_or_create(
        season=season,
        episode_number=i,
        defaults={
            'name': f'Episode {i}',
            'description': f'Test episode {i}',
            'release_date': timezone.now().date() - timedelta(days=10-i),
            'due_date': timezone.now().date() + timedelta(days=i*10),
        }
    )
    print(f'Episode: {episode.name} (ID: {episode.id})')

# Create titles
for i, name in enumerate(['Novice', 'Apprentice', 'Expert'], 1):
    rarity = ['common', 'rare', 'epic'][i-1]
    title, created = Title.objects.get_or_create(
        name=name,
        defaults={
            'description': f'{name} level title',
            'vault_credit_cost': i*100,
            'icon': f'{name.lower()}.png',
            'rarity': rarity
        }
    )
    print(f'Title: {title.name}')

print('Test data created!')
