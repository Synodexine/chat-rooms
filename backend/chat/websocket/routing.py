from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/chat/(?P<room_id>[0-9]*)/', consumers.ChatConsumer),
]
