from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def broadcast_to_group(group_name, event_type, data):
    """Helper function to broadcast events to WebSocket groups"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': event_type,
            'data': data
        }
    )


def notify_user(user_id, event_type, data):
    """Send notification to specific user"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user_id}',
        {
            'type': 'notification',
            'notification': {
                'event_type': event_type,
                **data
            }
        }
    )


def notify_mentor(mentor_id, event_type, data):
    """Send update to specific mentor"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'mentor_{mentor_id}',
        {
            'type': event_type,
            **data
        }
    )


def notify_student(student_id, event_type, data):
    """Send update to specific student"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'student_{student_id}',
        {
            'type': event_type,
            **data
        }
    )


def update_dashboard(event_type, data):
    """Broadcast dashboard updates to all connected admins/mentors"""
    broadcast_to_group('dashboard_updates', event_type, data)


def update_leaderboard(leaderboard_data):
    """Broadcast leaderboard updates"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'leaderboard_updates',
        {
            'type': 'leaderboard_update',
            'leaderboard': leaderboard_data
        }
    )


# Example signal handlers - Connect these in your apps

# @receiver(post_save, sender=YourSubmissionModel)
# def submission_created_handler(sender, instance, created, **kwargs):
#     if created:
#         # Notify mentor
#         if instance.mentor_id:
#             notify_mentor(
#                 instance.mentor_id,
#                 'student_submission',
#                 {
#                     'submission': {
#                         'id': instance.id,
#                         'student_name': instance.student.get_full_name(),
#                         'assignment': instance.assignment.title,
#                         'submitted_at': instance.created_at.isoformat()
#                     }
#                 }
#             )
#         
#         # Update dashboard
#         update_dashboard('submission_created', {
#             'submission_id': instance.id,
#             'student_id': instance.student_id
#         })


# @receiver(post_save, sender=YourGradeModel)
# def grade_updated_handler(sender, instance, created, **kwargs):
#     # Notify student
#     notify_student(
#         instance.student_id,
#         'grade_received',
#         {
#             'grade': {
#                 'assignment': instance.assignment.title,
#                 'score': instance.score,
#                 'feedback': instance.feedback
#             }
#         }
#     )
#     
#     # Update dashboard
#     update_dashboard('grade_updated', {
#         'grade_id': instance.id,
#         'student_id': instance.student_id
#     })
