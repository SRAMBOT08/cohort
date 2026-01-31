import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class DashboardConsumer(AsyncWebsocketConsumer):
    """Real-time dashboard updates for admin/mentor views"""
    
    async def connect(self):
        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Join dashboard group
        self.group_name = 'dashboard_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to dashboard updates'
        }))
    
    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'ping':
            await self.send(text_data=json.dumps({
                'type': 'pong',
                'timestamp': data.get('timestamp')
            }))
    
    async def dashboard_update(self, event):
        """Handle dashboard update events from channel layer"""
        await self.send(text_data=json.dumps({
            'type': 'dashboard_update',
            'data': event['data']
        }))
    
    async def submission_created(self, event):
        """Handle new submission events"""
        await self.send(text_data=json.dumps({
            'type': 'submission_created',
            'submission': event['submission']
        }))
    
    async def grade_updated(self, event):
        """Handle grade update events"""
        await self.send(text_data=json.dumps({
            'type': 'grade_updated',
            'grade': event['grade']
        }))


class NotificationConsumer(AsyncWebsocketConsumer):
    """Real-time notifications for individual users"""
    
    async def connect(self):
        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Each user has their own notification channel
        self.group_name = f'notifications_{self.user.id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send unread count on connection
        unread_count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'unread_count': unread_count
        }))
    
    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'mark_read':
            notification_id = data.get('notification_id')
            await self.mark_notification_read(notification_id)
    
    async def notification(self, event):
        """Handle notification events from channel layer"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))
    
    @database_sync_to_async
    def get_unread_count(self):
        """Get unread notification count for user"""
        # Implement based on your notification model
        return 0
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        # Implement based on your notification model
        pass


class LeaderboardConsumer(AsyncWebsocketConsumer):
    """Real-time leaderboard updates"""
    
    async def connect(self):
        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.group_name = 'leaderboard_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def leaderboard_update(self, event):
        """Handle leaderboard update events"""
        await self.send(text_data=json.dumps({
            'type': 'leaderboard_update',
            'leaderboard': event['leaderboard']
        }))


class MentorConsumer(AsyncWebsocketConsumer):
    """Real-time updates for mentor-specific data"""
    
    async def connect(self):
        self.user = self.scope["user"]
        self.mentor_id = self.scope['url_route']['kwargs']['mentor_id']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Verify user is the mentor or has permission
        if str(self.user.id) != self.mentor_id and not self.user.is_staff:
            await self.close()
            return
        
        self.group_name = f'mentor_{self.mentor_id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def student_submission(self, event):
        """Handle student submission events for this mentor"""
        await self.send(text_data=json.dumps({
            'type': 'student_submission',
            'submission': event['submission']
        }))
    
    async def review_request(self, event):
        """Handle review request events"""
        await self.send(text_data=json.dumps({
            'type': 'review_request',
            'request': event['request']
        }))


class StudentConsumer(AsyncWebsocketConsumer):
    """Real-time updates for student-specific data"""
    
    async def connect(self):
        self.user = self.scope["user"]
        self.student_id = self.scope['url_route']['kwargs']['student_id']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Verify user is the student or has permission
        if str(self.user.id) != self.student_id and not self.user.is_staff:
            await self.close()
            return
        
        self.group_name = f'student_{self.student_id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def grade_received(self, event):
        """Handle grade received events for this student"""
        await self.send(text_data=json.dumps({
            'type': 'grade_received',
            'grade': event['grade']
        }))
    
    async def feedback_received(self, event):
        """Handle feedback received events"""
        await self.send(text_data=json.dumps({
            'type': 'feedback_received',
            'feedback': event['feedback']
        }))
    
    async def achievement_unlocked(self, event):
        """Handle achievement unlock events"""
        await self.send(text_data=json.dumps({
            'type': 'achievement_unlocked',
            'achievement': event['achievement']
        }))
