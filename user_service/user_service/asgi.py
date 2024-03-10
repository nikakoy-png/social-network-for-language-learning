"""
ASGI config for user_service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import requests
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_service.settings')

application = get_asgi_application()
load_dotenv()

def register_service_in_registry():
    service_data = {
        'service_name': os.getenv('service_name'),
        'description': 'Description',
        'version_number': os.getenv('version_number'),
        'service_url': os.getenv('service_url')
    }

    registry_url = os.getenv('registry_service_url')

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
