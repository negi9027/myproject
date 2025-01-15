from django.urls import re_path
from .consumers import NotificationConsumer,CallingAgentConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<group_name>\w+)/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/callingagent/(?P<user_id>[\w-]+)/$', CallingAgentConsumer.as_asgi()),

]
