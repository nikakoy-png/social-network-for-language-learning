import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.db.models import Q

from celery_main import app


@app.task
def save_message_task(message, sender_id, dialog_id):
    from main.models import Message
    from main.serializer import MessageSerializer
    from asgiref.sync import sync_to_async

    msg = Message.objects.create(
        dialog_id=dialog_id,
        sender_id=sender_id,
        text=message,
        feedback=None
    )
    msg = MessageSerializer(msg)
    return msg.data


@app.task
def save_feedback_task(message_text, message_id, description, sender_id):
    from main.models import Feedback, Message
    from main.serializer import MessageSerializer

    from asgiref.sync import sync_to_async

    feedback = Feedback.objects.create(
        user_id=sender_id,
        correction_text=message_text,
        description=description
    )
    msg = Message.objects.get(pk=message_id)
    msg.feedback = feedback
    msg.save()
    msg = MessageSerializer(msg)
    return msg.data


class DialogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from main.models import UserDialog

        self.user = self.scope["user"]
        self.dialog_id = self.scope['url_route']['kwargs']['dialog_id']
        self.room_name = "dialog_%s" % self.dialog_id

        self.user_dialog: UserDialog | None = None
        self.companion_dialog: UserDialog | None = None

        try:
            self.user_dialog = await UserDialog.get_dialog_by_id(self.dialog_id, self.user.pk)
            self.companion_dialog = await UserDialog.get_companion_dialog_by_id(self.dialog_id, self.user.pk)
            print(self.companion_dialog)
        except UserDialog.DoesNotExist:
            await self.send(text_data=json.dumps({
                "type": "INFO",
                "message": "You are not in the dialog!"
            }))
            return None

        if await sync_to_async(UserDialog.func.is_user_in_dialog)(self.user.id):
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
            await self.send_last_messages(20)

    async def send_last_messages(self, num_messages):
        from main.models import Message
        from main.serializer import MessageSerializer

        self.user_dialog.unread_messages = 0
        await sync_to_async(self.user_dialog.save)()

        queryset = await sync_to_async(Message.objects.filter)(Q(dialog_id=self.dialog_id) & Q(is_deleted=False))

        messages = queryset.order_by('-send_date')[:num_messages]

        messages = await sync_to_async(list)(messages)

        print(messages[::-1])

        for message in messages[::-1]:
            serializer = MessageSerializer(message)
            serialized_message = await get_serialized_message(serializer)

            await self.send(text_data=json.dumps({
                'type': 'MESSAGE',
                'message': serialized_message,
            }))

    async def receive(self, text_data=None, bytes_data=None):
        from main.serializer import MessageSerializer
        from main.models import Message

        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'MESSAGE':
            sender_id = self.user.id
            message = text_data_json['message'] if text_data_json['message'] else None
            msg_task = save_message_task.delay(message, sender_id, self.dialog_id)

            # Ожидаем завершения задачи и получаем результат
            msg_result = msg_task.get()

            await sync_to_async(self.companion_dialog.increment_unread_messages)()
            # serializer = MessageSerializer(msg)
            # serialized_message = await get_serialized_message(serializer)

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat.message',
                    'message': msg_result,
                }
            )
            await update_list_dialogs_for_target_user(self.companion_dialog.user_id)
            await update_list_dialogs_for_target_user(sender_id)

        elif text_data_json['type'] == 'FEEDBACK':
            description = text_data_json['description']
            message_id = text_data_json['message_id']
            sender_id = self.user.id
            message = text_data_json['message'] if text_data_json['message'] else None

            fb_task = save_feedback_task.delay(sender_id=sender_id, message_text=message, description=description,
                                                message_id=message_id)

            fb_task = fb_task.get()

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat.feedback',
                    'message': fb_task,
                }
            )
        elif text_data_json['type'] == 'DELETE':
            message_id = text_data_json['message_id']
            message = await Message.objects.aget(id=message_id)
            message.is_deleted = True
            await sync_to_async(message.save)()

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat.delete',
                    'message': message_id,
                }
            )

    async def disconnect(self, close_code):
        self.user_dialog.unread_messages = 0
        await sync_to_async(self.user_dialog.save)()
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'MESSAGE',
            'message': message,
        }))

    async def chat_feedback(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'FEEDBACK',
            'message': message,
        }))

    async def chat_delete(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'DELETE',
            'message': message,
        }))

    async def save_message(self, message, sender_id):
        from main.models import Message
        msg = await Message.objects.acreate(dialog_id=self.dialog_id, sender_id=sender_id, text=message, feedback=None)
        return msg

    async def save_feedback(self, message_text: str, message_id, description, sender_id):
        from main.models import Feedback, Message
        feedback = await Feedback.objects.acreate(user_id=sender_id,
                                                  correction_text=message_text,
                                                  description=description)
        msg = await Message.objects.aget(pk=message_id)
        msg.feedback = feedback
        await sync_to_async(msg.save)()
        return msg

    async def INFO(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            "type": 'INFO',
            "message": message,
        }))


@sync_to_async
def get_serialized_message(serializer):
    return serializer.data


class DialogListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = f"dialog_list_{self.user.id}"

        print(self.user)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.get_dialog_list_and_send()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def get_dialog_list_and_send(self, user_id=None):
        dialog_list = await self.get_dialog_list(user_id)
        await self.send(text_data=json.dumps(dialog_list))

    @sync_to_async
    def get_dialog_list(self, _user_id=None):
        from main.models import UserDialog, Message

        dialog_list = []

        user_dialogs = UserDialog.objects.filter(user_id=self.user.id, is_deleted=False) \
            if not _user_id else UserDialog.objects.filter(user_id=_user_id, is_deleted=False)

        for user_dialog in user_dialogs:
            dialog = user_dialog.dialog
            last_message = Message.objects.filter(Q(dialog_id=dialog.id) & Q(is_deleted=False)).order_by('-send_date').first()
            dialog_companion = UserDialog.objects.filter(Q(dialog_id=dialog.id) & ~Q(user_id=self.user.id)).first() \
                if not _user_id else \
                UserDialog.objects.filter(Q(dialog_id=dialog.id) & ~Q(user_id=_user_id)).first()

            unread_messages = user_dialog.unread_messages
            companion_id = dialog_companion.user_id

            last_message_data = {
                "text": last_message.text if last_message else None,
                "sender_id": last_message.sender_id if last_message else None,
                "send_date": str(last_message.send_date if last_message else None)
            }

            dialog_data = {
                "dialog_id": dialog.id,
                "last_message": last_message_data if last_message_data else None,
                "created_at": str(dialog.created_at),
                "unread_messages": unread_messages,
                "companion_id": companion_id
            }
            dialog_list.append(dialog_data)

        return dialog_list

    async def update_dialog_list(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            "type": 'UPDATE_DIALOG_LIST',
            "data": data,
        }))


async def update_list_dialogs_for_target_user(user_id: int):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"dialog_list_{user_id}",
        {
            "type": "update.dialog.list",
            "data": await DialogListConsumer.get_dialog_list(user_id)
        }
    )
