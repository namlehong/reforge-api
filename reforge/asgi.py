import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import reforge.apps.poe.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reforge.settings.dev')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            reforge.apps.poe.routing.websocket_urlpatterns
        )
    ),
})