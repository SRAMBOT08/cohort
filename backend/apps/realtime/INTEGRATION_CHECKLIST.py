"""
IMPORTANT: Update your existing signal handlers to send real-time updates

Add these imports to your app's signals.py or models.py files:
"""

from apps.realtime.utils import (
    notify_dashboard,
    notify_mentor,
    notify_student,
    notify_user,
    update_leaderboard
)

# Example 1: When a student submits something (e.g., in apps/clt/models.py or signals.py)
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=YourSubmissionModel)
def submission_created(sender, instance, created, **kwargs):
    if created:
        # Notify mentor
        if hasattr(instance, 'mentor') and instance.mentor:
            notify_mentor(
                instance.mentor.id,
                'student_submission',
                {
                    'submission': {
                        'id': instance.id,
                        'student_name': instance.student.get_full_name(),
                        'title': instance.title,
                        'submitted_at': instance.created_at.isoformat()
                    }
                }
            )
        
        # Update dashboard
        notify_dashboard('submission_created', {
            'submission': {
                'id': instance.id,
                'student_id': instance.student.id
            }
        })
"""

# Example 2: When gamification points are awarded (apps/gamification/models.py or signals.py)
"""
@receiver(post_save, sender=GamificationPoints)
def points_awarded(sender, instance, created, **kwargs):
    if created:
        # Notify the user
        notify_user(
            instance.user.id,
            {
                'title': f'+{instance.points} Points!',
                'message': instance.reason,
                'type': 'points',
                'points': instance.points
            }
        )
        
        # Trigger leaderboard recalculation
        from apps.gamification.utils import get_leaderboard_data
        leaderboard = get_leaderboard_data()
        update_leaderboard(leaderboard)
"""

# Example 3: When a mentor provides feedback (apps/cfc/models.py or similar)
"""
@receiver(post_save, sender=Feedback)
def feedback_provided(sender, instance, created, **kwargs):
    if created:
        # Notify student
        notify_student(
            instance.student.id,
            'feedback_received',
            {
                'feedback': {
                    'id': instance.id,
                    'submission': instance.submission.title,
                    'mentor': instance.mentor.get_full_name(),
                    'message': instance.message
                }
            }
        )
"""

# Example 4: Announcement system (apps/dashboard/views.py)
"""
from rest_framework.decorators import api_view
from apps.realtime.utils import notify_user

@api_view(['POST'])
def create_announcement(request):
    title = request.data.get('title')
    message = request.data.get('message')
    recipient_ids = request.data.get('recipients', [])
    
    # Save announcement to database
    # ...
    
    # Send real-time notification
    for user_id in recipient_ids:
        notify_user(user_id, {
            'title': title,
            'message': message,
            'type': 'announcement'
        })
    
    return Response({'status': 'sent'})
"""
