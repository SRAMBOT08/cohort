#!/usr/bin/env python3
"""
Check season scores in database
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.gamification.models import SeasonScore, Season

User = get_user_model()

def main():
    print("=" * 60)
    print("SEASON SCORES CHECK")
    print("=" * 60)
    
    # Get all season scores
    all_scores = SeasonScore.objects.all().select_related('student', 'season')
    
    print(f"\nTotal Season Scores: {all_scores.count()}\n")
    
    for score in all_scores:
        print(f"User: {score.student.username}")
        print(f"Season: {score.season.name}")
        print(f"Total Score: {score.total_score}/1500")
        print(f"Completed: {score.season_completed}")
        print(f"  CLT: {score.clt_score}, IIPC: {score.iipc_score}, CFC: {score.cfc_score}")
        print(f"  SCD: {score.scd_score}, Outcome: {score.outcome_score}")
        print("-" * 60)
    
    # Check active seasons
    print("\n" + "=" * 60)
    print("ACTIVE SEASONS")
    print("=" * 60)
    seasons = Season.objects.all()
    for season in seasons:
        print(f"Season {season.season_number}: {season.name}")
        print(f"  Active: {season.is_active}")
        print(f"  Start: {season.start_date}, End: {season.end_date}")
        print("-" * 60)

if __name__ == '__main__':
    main()
