from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class Command(BaseCommand):
    help = 'Test WebSocket channel layer and Redis connection'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing WebSocket and Redis setup...'))
        
        channel_layer = get_channel_layer()
        
        if channel_layer is None:
            self.stdout.write(self.style.ERROR('✗ Channel layer is not configured!'))
            return
        
        self.stdout.write(self.style.SUCCESS('✓ Channel layer configured'))
        
        # Test Redis connection
        try:
            test_channel = 'test_channel'
            test_message = {'type': 'test.message', 'text': 'Hello from Django!'}
            
            # Send message
            async_to_sync(channel_layer.send)(test_channel, test_message)
            self.stdout.write(self.style.SUCCESS('✓ Successfully sent message to channel layer'))
            
            # Test group operations
            group_name = 'test_group'
            channel_name = 'test_channel_name'
            
            async_to_sync(channel_layer.group_add)(group_name, channel_name)
            self.stdout.write(self.style.SUCCESS(f'✓ Added channel to group: {group_name}'))
            
            async_to_sync(channel_layer.group_send)(
                group_name,
                {'type': 'test_message', 'data': 'test'}
            )
            self.stdout.write(self.style.SUCCESS('✓ Sent message to group'))
            
            async_to_sync(channel_layer.group_discard)(group_name, channel_name)
            self.stdout.write(self.style.SUCCESS(f'✓ Removed channel from group'))
            
            self.stdout.write(self.style.SUCCESS('\n✓ All tests passed! WebSocket setup is working correctly.'))
            self.stdout.write(self.style.SUCCESS('\nNext steps:'))
            self.stdout.write('1. Start Redis: redis-server')
            self.stdout.write('2. Run server: daphne config.asgi:application')
            self.stdout.write('3. Connect from frontend: ws://localhost:8000/ws/dashboard/?token=YOUR_JWT')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
            self.stdout.write(self.style.WARNING('\nTroubleshooting:'))
            self.stdout.write('1. Check if Redis is running: redis-cli ping')
            self.stdout.write('2. Verify REDIS_URL in .env file')
            self.stdout.write('3. Install Redis: brew install redis (macOS) or apt install redis (Linux)')
