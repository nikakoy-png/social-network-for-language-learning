# tasks.py
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
from django.db.models import Q


@shared_task
def save_message_async(dialog_id, sender_id, message):
    from main.models import Message
    from main.serializer import MessageSerializer

    # Сохраняем сообщение асинхронно
    msg = sync_to_async(Message.objects.acreate)(dialog_id=dialog_id, sender_id=sender_id, text=message, feedback=None)

    # Получаем сериализованное сообщение
    serializer = sync_to_async(MessageSerializer)(msg)
    serialized_message = sync_to_async(get_serialized_message)(serializer)

    return serialized_message


@shared_task
def update_dialog_list_async(user_id):
    from main.models import UserDialog, Message
    from main.serializer import MessageSerializer

    # Получаем список диалогов асинхронно
    dialog_list = sync_to_async(get_dialog_list)(user_id)

    # Обновляем список диалогов в соответствующей группе
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"dialog_list_{user_id}",
        {
            "type": "update.dialog.list",
            "data": dialog_list
        }
    )

    return dialog_list


@sync_to_async
def get_serialized_message(serializer):
    return serializer.data


@sync_to_async
def get_dialog_list(user_id=None):
    from main.models import UserDialog, Message

    dialog_list = []

    user_dialogs = UserDialog.objects.filter(user_id=user_id, is_deleted=False)

    for user_dialog in user_dialogs:
        dialog = user_dialog.dialog
        last_message = Message.objects.filter(Q(dialog_id=dialog.id) & Q(is_deleted=False)).order_by(
            '-send_date').first()
        dialog_companion = UserDialog.objects.filter(Q(dialog_id=dialog.id) & ~Q(user_id=user_id)).first()

        unread_messages = user_dialog.unread_messages
        companion_id = dialog_companion.user_id if dialog_companion else None

        last_message_data = {
            "text": last_message.text if last_message else None,
            "sender_id": last_message.sender_id if last_message else None,
            "send_date": str(last_message.send_date) if last_message else None
        }

        dialog_data = {
            "dialog_id": dialog.id,
            "last_message": last_message_data,
            "created_at": str(dialog.created_at),
            "unread_messages": unread_messages,
            "companion_id": companion_id
        }
        dialog_list.append(dialog_data)

    return dialog_list
