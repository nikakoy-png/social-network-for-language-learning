from django.urls import re_path
from main import consumers

websocket_urlpatterns = [
    re_path(r"ws/dialog/(?P<dialog_id>\w+)/$", consumers.DialogConsumer.as_asgi()),
    re_path(r"ws/dialogs/", consumers.DialogListConsumer.as_asgi()),
]