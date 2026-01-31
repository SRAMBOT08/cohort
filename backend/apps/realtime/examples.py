"""
Example: How to trigger real-time updates from your views/APIs

This file demonstrates how to integrate WebSocket notifications
into your existing REST API endpoints.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.realtime.utils import (
    notify_dashboard,
    notify_mentor,
    notify_student,
    notify_user,
    update_leaderboard
)


# Example 1: Student submits an assignment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_assignment(request, assignment_id):
    """
    When a student submits an assignment, notify:
    1. The assigned mentor
    2. The dashboard
    3. The student (confirmation)
    """
    user = request.user
    
    # Your existing submission logic
    # submission = Submission.objects.create(...)
    
    # Real-time notifications
    if hasattr(user, 'mentor') and user.mentor:
        notify_mentor(
            user.mentor.id,
            'student_submission',
            {
                'submission': {
                    'id': 123,  # submission.id
                    'student_name': user.get_full_name(),
                    'assignment_title': 'Assignment Title',
                    'submitted_at': 'timestamp'
                }
            }
        )
    
    # Update dashboard
    notify_dashboard(
        'submission_created',
        {
            'submission': {
                'id': 123,
                'student_id': user.id,
                'assignment_id': assignment_id
            }
        }
    )
    
    # Confirm to student
    notify_user(
        user.id,
        {
            'title': 'Submission Received',
            'message': 'Your assignment has been submitted successfully',
            'type': 'success'
        }
    )
    
    return Response({'status': 'submitted'}, status=status.HTTP_201_CREATED)


# Example 2: Mentor grades a submission
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def grade_submission(request, submission_id):
    """
    When a mentor grades a submission, notify:
    1. The student
    2. The dashboard
    """
    mentor = request.user
    grade = request.data.get('grade')
    feedback = request.data.get('feedback')
    
    # Your existing grading logic
    # submission = Submission.objects.get(id=submission_id)
    # submission.grade = grade
    # submission.save()
    
    student_id = 456  # submission.student.id
    
    # Notify student of new grade
    notify_student(
        student_id,
        'grade_received',
        {
            'grade': {
                'assignment': 'Assignment Title',
                'score': grade,
                'feedback': feedback,
                'graded_by': mentor.get_full_name()
            }
        }
    )
    
    # Update dashboard
    notify_dashboard(
        'grade_updated',
        {
            'grade': {
                'submission_id': submission_id,
                'student_id': student_id,
                'grade': grade
            }
        }
    )
    
    return Response({'status': 'graded'}, status=status.HTTP_200_OK)


# Example 3: Leaderboard recalculation
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recalculate_leaderboard(request):
    """
    When leaderboard is recalculated, broadcast to all connected clients
    """
    # Your leaderboard calculation logic
    leaderboard_data = [
        {'rank': 1, 'user_id': 1, 'name': 'John Doe', 'points': 1500},
        {'rank': 2, 'user_id': 2, 'name': 'Jane Smith', 'points': 1450},
        # ... more entries
    ]
    
    # Broadcast to all leaderboard viewers
    update_leaderboard(leaderboard_data)
    
    return Response({'status': 'updated'}, status=status.HTTP_200_OK)


# Example 4: Gamification - Achievement unlocked
def unlock_achievement(user_id, achievement_data):
    """
    Called from your gamification system when user earns achievement
    """
    notify_student(
        user_id,
        'achievement_unlocked',
        {
            'achievement': {
                'id': achievement_data['id'],
                'title': achievement_data['title'],
                'description': achievement_data['description'],
                'points': achievement_data['points'],
                'badge_url': achievement_data['badge_url']
            }
        }
    )
    
    # Also send general notification
    notify_user(
        user_id,
        {
            'title': 'Achievement Unlocked!',
            'message': f"You earned: {achievement_data['title']}",
            'type': 'achievement',
            'points': achievement_data['points']
        }
    )


# Example 5: Bulk notifications
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_announcement(request):
    """
    Send announcement to multiple users
    """
    message = request.data.get('message')
    recipient_ids = request.data.get('recipients', [])
    
    notification_data = {
        'title': 'New Announcement',
        'message': message,
        'type': 'announcement',
        'sender': request.user.get_full_name()
    }
    
    # Send to all recipients
    for user_id in recipient_ids:
        notify_user(user_id, notification_data)
    
    return Response({'status': 'sent', 'count': len(recipient_ids)})
