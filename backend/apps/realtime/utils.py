"""
Utility functions for triggering real-time updates from anywhere in the application
"""
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class RealtimeNotifier:
    """Helper class for sending real-time updates"""
    
    def __init__(self):
        self.channel_layer = get_channel_layer()
    
    def _send_to_group(self, group_name, message_type, data):
        """Send message to a WebSocket group"""
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type': message_type,
                **data
            }
        )
    
    def notify_dashboard(self, event_type, data):
        """
        Send update to dashboard
        
        Usage:
            notifier = RealtimeNotifier()
            notifier.notify_dashboard('submission_created', {
                'submission': {'id': 123, 'student': 'John Doe'}
            })
        """
        self._send_to_group('dashboard_updates', event_type, data)
    
    def notify_user(self, user_id, notification_data):
        """
        Send notification to specific user
        
        Usage:
            notifier = RealtimeNotifier()
            notifier.notify_user(user_id, {
                'title': 'New Grade',
                'message': 'You received a grade for Assignment 1',
                'type': 'grade'
            })
        """
        self._send_to_group(
            f'notifications_{user_id}',
            'notification',
            {'notification': notification_data}
        )
    
    def notify_mentor(self, mentor_id, event_type, data):
        """
        Send update to specific mentor
        
        Usage:
            notifier = RealtimeNotifier()
            notifier.notify_mentor(mentor_id, 'student_submission', {
                'submission': {...}
            })
        """
        self._send_to_group(f'mentor_{mentor_id}', event_type, data)
    
    def notify_student(self, student_id, event_type, data):
        """
        Send update to specific student
        
        Usage:
            notifier = RealtimeNotifier()
            notifier.notify_student(student_id, 'grade_received', {
                'grade': {...}
            })
        """
        self._send_to_group(f'student_{student_id}', event_type, data)
    
    def update_leaderboard(self, leaderboard_data):
        """
        Broadcast leaderboard updates to all connected clients
        
        Usage:
            notifier = RealtimeNotifier()
            notifier.update_leaderboard([
                {'rank': 1, 'name': 'John', 'points': 100},
                {'rank': 2, 'name': 'Jane', 'points': 95}
            ])
        """
        self._send_to_group(
            'leaderboard_updates',
            'leaderboard_update',
            {'leaderboard': leaderboard_data}
        )


# Convenience functions for direct import
notifier = RealtimeNotifier()

def notify_dashboard(event_type, data):
    """Shortcut: Send dashboard update"""
    notifier.notify_dashboard(event_type, data)

def notify_user(user_id, notification_data):
    """Shortcut: Send user notification"""
    notifier.notify_user(user_id, notification_data)

def notify_mentor(mentor_id, event_type, data):
    """Shortcut: Send mentor update"""
    notifier.notify_mentor(mentor_id, event_type, data)

def notify_student(student_id, event_type, data):
    """Shortcut: Send student update"""
    notifier.notify_student(student_id, event_type, data)

def update_leaderboard(leaderboard_data):
    """Shortcut: Update leaderboard"""
    notifier.update_leaderboard(leaderboard_data)
