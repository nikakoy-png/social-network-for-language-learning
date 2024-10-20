"""
ASGI config for communication_service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import requests

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from communication_service.authentication import WebSocketTokenAuthMiddleware
from main.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communication_service.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
           WebSocketTokenAuthMiddleware(
                AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
            )
        ),
    }
)


def register_service_in_registry():
    service_data = {
        'service_name': os.environ.get('service_name'),
        'description': 'Description',
        'version_number': os.environ.get('version_number'),
        'service_url': os.environ.get('service_url')
    }

    registry_url = os.environ.get('registry_service_url')

    try:
        response = requests.post(registry_url, json=service_data)
        response.raise_for_status()
        print(f"The radio now includes the “communicator” service: {response.status_code}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
register_service_in_registry()