#!/usr/bin/env python3
import os
import sys

# Setup Django path
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cohort.settings')

import django
django.setup()

from django.contrib.auth.models import User
from apps.scd.models import LeetCodeProfile
from django.utils import timezone

# Get test students
students = User.objects.filter(username__in=['teststudent1', 'teststudent2'])
print(f"Found {students.count()} students")

for student in students:
    profile, created = LeetCodeProfile.objects.get_or_create(
        user=student,
        defaults={
            'leetcode_username': f'{student.username}_lc',
            'total_solved': 150 + (student.id % 50),
            'easy_solved': 80 + (student.id % 20),
            'medium_solved': 50 + (student.id % 20),
            'hard_solved': 20 + (student.id % 10),
            'streak': 15 + (student.id % 10),
            'ranking': 50000 + (student.id * 100),
            'total_active_days': 100 + (student.id % 30),
            'monthly_problems_count': 12,
            'submission_calendar': {},
            'last_synced': timezone.now(),
            'status': 'pending',
            'submitted_at': timezone.now(),
        }
    )
    if created:
        print(f'✅ Created LeetCode profile for {student.username}: {profile.leetcode_username} ({profile.total_solved} problems, status: {profile.status})')
    else:
        print(f'⚠️  Profile already exists for {student.username}')

# Verify
total = LeetCodeProfile.objects.count()
pending = LeetCodeProfile.objects.filter(status='pending').count()
print(f"\n📊 Total profiles: {total}, Pending: {pending}")
