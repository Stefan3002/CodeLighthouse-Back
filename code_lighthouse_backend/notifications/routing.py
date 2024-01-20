from django.urls import path

from code_lighthouse_backend.notifications import consumers

websocket_urlpatterns = [
    path(r'ws/socket-server', consumers.NotificationConsumer.as_asgi())
]