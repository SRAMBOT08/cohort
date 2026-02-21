#!/usr/bin/env python3
"""
Sync Episode Progress with Actual Pillar Submissions
This script syncs the gamification episode progress with actual approved submissions
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.gamification.models import Season, Episode, EpisodeProgress
from apps.gamification.services import EpisodeService, SeasonScoringService
from apps.clt.models import CLTSubmission
from apps.cfc.models import HackathonSubmission, BMCVideoSubmission, GenAIProjectSubmission
from apps.iipc.models import LinkedInPostVerification, LinkedInConnectionVerification
from apps.scd.models import LeetCodeProfile
from apps.sri.models import SRISubmission

User = get_user_model()


def sync_user_episode_progress(user):
    """Sync a single user's episode progress based on their submissions"""
    print(f"\n{'='*60}")
    print(f"Syncing episode progress for: {user.username}")
    print(f"{'='*60}")
    
    current_season = Season.objects.filter(is_active=True).first()
    if not current_season:
        print("❌ No active season found")
        return
    
    print(f"✓ Active season: {current_season.name}")
    
    # Get all episodes for the season
    episodes = Episode.objects.filter(season=current_season).order_by('episode_number')
    
    for episode in episodes:
        episode_num = episode.episode_number
        print(f"\n📍 Episode {episode_num}: {episode.name}")
        
        # Get or create episode progress
        progress, created = EpisodeProgress.objects.get_or_create(
            student=user,
            episode=episode
        )
        
        if created:
            print(f"  Created new episode progress record")
        
        # Track changes
        tasks_updated = []
        
        # EPISODE 1: CLT + SCD Streak
        if episode_num == 1:
            # Check CLT (1 approved submission)
            clt_approved = CLTSubmission.objects.filter(
                user=user, 
                status='approved'
            ).exists()
            
            if clt_approved and not progress.clt_completed:
                EpisodeService.mark_task_completed(user, episode, 'clt')
                tasks_updated.append('CLT')
                print(f"  ✓ Marked CLT as completed")
            elif progress.clt_completed:
                print(f"  ✓ CLT already completed")
            else:
                print(f"  ⚪ CLT not yet completed")
            
            # Check SCD Streak (LeetCode profile with problems)
            leetcode_profile = LeetCodeProfile.objects.filter(
                user=user,
                total_solved__gte=10
            ).exists()
            
            if leetcode_profile and not progress.scd_streak_active:
                EpisodeService.mark_task_completed(user, episode, 'scd_streak')
                tasks_updated.append('SCD Streak')
                print(f"  ✓ Marked SCD Streak as active")
            elif progress.scd_streak_active:
                print(f"  ✓ SCD Streak already active")
            else:
                print(f"  ⚪ SCD Streak not active (need 10+ problems)")
        
        # EPISODE 2: CFC Task 1 (Hackathon) + IIPC Task 1 (LinkedIn Post) + SCD
        elif episode_num == 2:
            # Check CFC Task 1 (Hackathon)
            hackathon_approved = HackathonSubmission.objects.filter(
                user=user,
                status='approved'
            ).exists()
            
            if hackathon_approved and not progress.cfc_task1_completed:
                EpisodeService.mark_task_completed(user, episode, 'cfc_task1')
                tasks_updated.append('CFC Task 1 (Hackathon)')
                print(f"  ✓ Marked CFC Task 1 as completed")
            elif progress.cfc_task1_completed:
                print(f"  ✓ CFC Task 1 already completed")
            else:
                print(f"  ⚪ CFC Task 1 not yet completed")
            
            # Check IIPC Task 1 (LinkedIn Post)
            linkedin_post = LinkedInPostVerification.objects.filter(
                user=user,
                status='approved'
            ).exists()
            
            if linkedin_post and not progress.iipc_task1_completed:
                EpisodeService.mark_task_completed(user, episode, 'iipc_task1')
                tasks_updated.append('IIPC Task 1 (LinkedIn Post)')
                print(f"  ✓ Marked IIPC Task 1 as completed")
            elif progress.iipc_task1_completed:
                print(f"  ✓ IIPC Task 1 already completed")
            else:
                print(f"  ⚪ IIPC Task 1 not yet completed")
            
            # Check SCD Streak
            leetcode_profile = LeetCodeProfile.objects.filter(
                user=user,
                total_solved__gte=10
            ).exists()
            
            if leetcode_profile and not progress.scd_streak_active:
                EpisodeService.mark_task_completed(user, episode, 'scd_streak')
                tasks_updated.append('SCD Streak')
                print(f"  ✓ Marked SCD Streak as active")
            elif progress.scd_streak_active:
                print(f"  ✓ SCD Streak already active")
        
        # EPISODE 3: CFC Task 2 (BMC Video) + IIPC Task 2 (LinkedIn Connection) + SCD
        elif episode_num == 3:
            # Check CFC Task 2 (BMC Video)
            bmc_approved = BMCVideoSubmission.objects.filter(
                user=user,
                status='approved'
            ).exists()
            
            if bmc_approved and not progress.cfc_task2_completed:
                EpisodeService.mark_task_completed(user, episode, 'cfc_task2')
                tasks_updated.append('CFC Task 2 (BMC Video)')
                print(f"  ✓ Marked CFC Task 2 as completed")
            elif progress.cfc_task2_completed:
                print(f"  ✓ CFC Task 2 already completed")
            else:
                print(f"  ⚪ CFC Task 2 not yet completed")
            
            # Check IIPC Task 2 (LinkedIn Connection)
            linkedin_connection = LinkedInConnectionVerification.objects.filter(
                user=user,
                status='approved'
            ).exists()
            
            if linkedin_connection and not progress.iipc_task2_completed:
                EpisodeService.mark_task_completed(user, episode, 'iipc_task2')
                tasks_updated.append('IIPC Task 2 (LinkedIn Connection)')
                print(f"  ✓ Marked IIPC Task 2 as completed")
            elif progress.iipc_task2_completed:
                print(f"  ✓ IIPC Task 2 already completed")
            else:
                print(f"  ⚪ IIPC Task 2 not yet completed")
            
            # Check SCD Streak
            leetcode_profile = LeetCodeProfile.objects.filter(
                user=user,
                total_solved__gte=10
            ).exists()
            
            if leetcode_profile and not progress.scd_streak_active:
                EpisodeService.mark_task_completed(user, episode, 'scd_streak')
                tasks_updated.append('SCD Streak')
                print(f"  ✓ Marked SCD Streak as active")
            elif progress.scd_streak_active:
                print(f"  ✓ SCD Streak already active")
        
        # EPISODE 4: CFC Task 3 (GenAI Project) + SRI + SCD
        elif episode_num == 4:
            # Check CFC Task 3 (GenAI Project)
            genai_approved = GenAIProjectSubmission.objects.filter(
                user=user,
                status='approved'
            ).exists()
            
            if genai_approved and not progress.cfc_task3_completed:
                EpisodeService.mark_task_completed(user, episode, 'cfc_task3')
                tasks_updated.append('CFC Task 3 (GenAI Project)')
                print(f"  ✓ Marked CFC Task 3 as completed")
            elif progress.cfc_task3_completed:
                print(f"  ✓ CFC Task 3 already completed")
            else:
                print(f"  ⚪ CFC Task 3 not yet completed")
            
            # Check SRI (at least 1 approved activity)
            sri_approved = SRISubmission.objects.filter(
                user=user,
                status='approved'
            ).exists()
            
            if sri_approved and not progress.sri_completed:
                EpisodeService.mark_task_completed(user, episode, 'sri')
                tasks_updated.append('SRI')
                print(f"  ✓ Marked SRI as completed")
            elif progress.sri_completed:
                print(f"  ✓ SRI already completed")
            else:
                print(f"  ⚪ SRI not yet completed (need 1 approved activity)")
            
            # Check SCD Streak
            leetcode_profile = LeetCodeProfile.objects.filter(
                user=user,
                total_solved__gte=10
            ).exists()
            
            if leetcode_profile and not progress.scd_streak_active:
                EpisodeService.mark_task_completed(user, episode, 'scd_streak')
                tasks_updated.append('SCD Streak')
                print(f"  ✓ Marked SCD Streak as active")
            elif progress.scd_streak_active:
                print(f"  ✓ SCD Streak already active")
        
        # Unlock episode if it's locked but previous episodes are complete
        if progress.status == 'locked' and episode_num > 1:
            prev_episode = Episode.objects.filter(
                season=current_season,
                episode_number=episode_num - 1
            ).first()
            
            if prev_episode:
                prev_progress = EpisodeProgress.objects.filter(
                    student=user,
                    episode=prev_episode,
                    status='completed'
                ).exists()
                
                if prev_progress:
                    progress.status = 'unlocked'
                    progress.save()
                    print(f"  🔓 Unlocked episode {episode_num}")
        
        # Refresh progress to get updated completion percentage
        progress.refresh_from_db()
        print(f"  📊 Episode {episode_num} Progress: {progress.status}")
        
        if tasks_updated:
            print(f"  ✨ Tasks updated this sync: {', '.join(tasks_updated)}")
    
    # Update season score after all episodes synced
    print(f"\n💰 Updating season score...")
    season_score = SeasonScoringService.update_season_score(user, current_season)
    print(f"  Season Score: {season_score.total_score}/1500")
    print(f"    CLT: {season_score.clt_score}, IIPC: {season_score.iipc_score}, SCD: {season_score.scd_score}")
    print(f"    CFC: {season_score.cfc_score}, Outcome: {season_score.outcome_score}")
    
    print(f"\n{'='*60}")
    print(f"✓ Sync complete for {user.username}")
    print(f"{'='*60}\n")


def sync_all_students():
    """Sync episode progress for all students"""
    print("\n" + "="*60)
    print("SYNCING EPISODE PROGRESS FOR ALL STUDENTS")
    print("="*60)
    
    # Get all users with student role
    students = User.objects.filter(
        Q(profile__role='STUDENT') | Q(profile__isnull=True)
    ).exclude(is_superuser=True)
    
    print(f"\nFound {students.count()} students to sync\n")
    
    for student in students:
        try:
            sync_user_episode_progress(student)
        except Exception as e:
            print(f"❌ Error syncing {student.username}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("SYNC COMPLETE")
    print("="*60 + "\n")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Sync episode progress with pillar submissions')
    parser.add_argument('--user', help='Sync specific user by username')
    parser.add_argument('--all', action='store_true', help='Sync all students')
    
    args = parser.parse_args()
    
    if args.user:
        try:
            user = User.objects.get(username=args.user)
            sync_user_episode_progress(user)
        except User.DoesNotExist:
            print(f"❌ User '{args.user}' not found")
            sys.exit(1)
    elif args.all:
        sync_all_students()
    else:
        # If no arguments, show usage
        parser.print_help()
        print("\nExample usage:")
        print("  python3 sync_episode_progress.py --user student123")
        print("  python3 sync_episode_progress.py --all")
