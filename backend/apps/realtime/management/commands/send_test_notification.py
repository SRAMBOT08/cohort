from django.core.management.base import BaseCommand
from apps.realtime.utils import (
    notify_dashboard,
    notify_user,
    update_leaderboard
)


class Command(BaseCommand):
    help = 'Send test real-time notifications to verify WebSocket functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='User ID to send test notification to',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Sending test notifications...'))
        
        # Test dashboard update
        try:
            notify_dashboard('test_event', {
                'message': 'Test dashboard update',
                'timestamp': 'now'
            })
            self.stdout.write(self.style.SUCCESS('✓ Sent test dashboard update'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Dashboard update failed: {str(e)}'))
        
        # Test user notification (if user_id provided)
        user_id = options.get('user_id')
        if user_id:
            try:
                notify_user(user_id, {
                    'title': 'Test Notification',
                    'message': 'This is a test notification from the backend',
                    'type': 'test'
                })
                self.stdout.write(self.style.SUCCESS(f'✓ Sent test notification to user {user_id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ User notification failed: {str(e)}'))
        
        # Test leaderboard update
        try:
            test_leaderboard = [
                {'rank': 1, 'name': 'Test User 1', 'points': 100},
                {'rank': 2, 'name': 'Test User 2', 'points': 90},
                {'rank': 3, 'name': 'Test User 3', 'points': 80},
            ]
            update_leaderboard(test_leaderboard)
            self.stdout.write(self.style.SUCCESS('✓ Sent test leaderboard update'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Leaderboard update failed: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Test notifications sent!'))
        self.stdout.write('Check your WebSocket clients to verify they received the messages.')
