#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gamification.models import Season, PercentileBracket
from apps.profiles.models import UserProfile

season = Season.objects.first()
all_students = UserProfile.objects.filter(role='STUDENT')
top_3 = list(all_students[:3].values_list('user_id', flat=True))
others = all_students.exclude(user_id__in=top_3)

print(f'Creating {others.count()} percentile entries...')
for i, student in enumerate(others):
    bracket, created = PercentileBracket.objects.get_or_create(
        season=season,
        student=student.user,
        defaults={
            'percentile_range': f'{(i+1)*10}%',
            'season_score': 600 - (i * 100)
        }
    )
    status = 'Created' if created else 'Exists'
    print(f'  {status} - {student.user.username}: {bracket.percentile_range}')

print(f'\nTotal percentile entries: {PercentileBracket.objects.filter(season=season).count()}')
