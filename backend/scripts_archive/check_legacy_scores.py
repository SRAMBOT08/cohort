#!/usr/bin/env python3
"""
Check and recalculate legacy scores
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.gamification.models import LegacyScore, SeasonScore

User = get_user_model()

def main():
    print("=" * 60)
    print("LEGACY SCORE RECALCULATION")
    print("=" * 60)
    
    # Get all users with season scores (not just completed)
    users_with_scores = User.objects.filter(
        season_scores__isnull=False
    ).distinct()
    
    print(f"\nFound {users_with_scores.count()} users with season scores\n")
    
    for user in users_with_scores:
        print(f"\n{'='*60}")
        print(f"User: {user.username}")
        print(f"{'='*60}")
        
        # Get season scores (all, not just completed)
        season_scores = SeasonScore.objects.filter(
            student=user
        ).order_by('season__season_number')
        
        print(f"\nSeason Scores:")
        total_from_seasons = 0
        for ss in season_scores:
            print(f"  Season {ss.season.season_number}: {ss.total_score} points")
            total_from_seasons += ss.total_score
        
        print(f"\nTotal from Seasons: {total_from_seasons}")
        
        # Get or create legacy score
        legacy_score, created = LegacyScore.objects.get_or_create(student=user)
        
        print(f"\nLegacy Score BEFORE recalculation:")
        print(f"  Total Legacy Points: {legacy_score.total_legacy_points}")
        print(f"  Ascension Bonus: {legacy_score.ascension_bonus_total}")
        print(f"  Seasons Completed: {legacy_score.seasons_completed}")
        
        # Recalculate
        legacy_score.recalculate_from_season_scores()
        
        print(f"\nLegacy Score AFTER recalculation:")
        print(f"  Total Legacy Points: {legacy_score.total_legacy_points}")
        print(f"  Ascension Bonus: {legacy_score.ascension_bonus_total}")
        print(f"  Seasons Completed: {legacy_score.seasons_completed}")
        print(f"  Highest Season Score: {legacy_score.highest_season_score}")
        print(f"  Last Season Score: {legacy_score.last_season_score}")
    
    print(f"\n{'='*60}")
    print("✓ Recalculation complete!")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
