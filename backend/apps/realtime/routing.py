from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dashboard/$', consumers.DashboardConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/leaderboard/$', consumers.LeaderboardConsumer.as_asgi()),
    re_path(r'ws/mentor/(?P<mentor_id>\w+)/$', consumers.MentorConsumer.as_asgi()),
    re_path(r'ws/student/(?P<student_id>\w+)/$', consumers.StudentConsumer.as_asgi()),
]
