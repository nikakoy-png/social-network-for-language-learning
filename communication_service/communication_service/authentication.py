import os

import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from channels.middleware import BaseMiddleware
import requests
from django.contrib.auth import get_user_model
import logging
import requests

from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)


class WebSocketTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from main.models import User

        try:
            print(scope)
            cookies = dict(scope["headers"]).get(b"cookie", b"").decode("utf-8")
            print(cookies)
            token = None
            if cookies:
                cookie_items = cookies.split(";")
                for item in cookie_items:
                    if item.strip().startswith("token="):
                        token = item.strip().split("=")[1]
                        break

            if token:
                try:
                    user_service_url = f'{os.getenv('user_service_url')}user/profile/'
                    headers = {'Authorization': 'Bearer {}'.format(token)}
                    response = requests.get(url=user_service_url, headers=headers)
                    if response.status_code == 200:
                        user_data = response.json()
                        del user_data["languages"]
                        user = User(**user_data)
                        scope["user"] = user
                        logger.info(f"User {user.username} fetched successfully")
                    else:
                        logger.error(f"Failed to fetch user data. Status code: {response.status_code}")
                except requests.RequestException as e:
                    logger.exception(f"RequestException occurred: {str(e)}")

        except jwt.exceptions.InvalidTokenError:
            pass

        return await super().__call__(scope, receive, send)

import os
import jwt
import requests
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

from dotenv import load_dotenv
load_dotenv()


class HttpRequestTokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        from main.models import User


        token = self.get_token_from_request(request)
        if token:
            try:
                user_service_url = f'{os.environ.get("user_service_url")}user/profile/'
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(url=user_service_url, headers=headers)
                if response.status_code == 200:
                    user_data = response.json()
                    del user_data["languages"]
                    user = User(**user_data)
                    request.user = user
                else:
                    raise exceptions.AuthenticationFailed("Failed to authenticate user")
            except requests.RequestException:
                raise exceptions.AuthenticationFailed("Failed to authenticate user")

        response = self.get_response(request, *args, **kwargs)
        return response

    def get_token_from_request(self, request):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        return token
