from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/poe$', consumers.PoeConsumer.as_asgi()),
]