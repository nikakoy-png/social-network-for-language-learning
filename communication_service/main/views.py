import datetime
import os
from functools import wraps

from asgiref.sync import sync_to_async
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response

from .consumers import DialogListConsumer, update_list_dialogs_for_target_user
from .models import Dialog, UserDialog, Message, Feedback, Complaint
import json
import httpx
from adrf.decorators import api_view
from django.http import JsonResponse
from .models import Dialog, UserDialog, Message
import json

from .serializer import ComplaintSerializer, DialogSerializer, UserDialogSerializer, MessageSerializer, \
    ResolutionSerializer


@api_view(['POST'])
async def create_dialog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_ids = data.get('user_ids')

            if not user_ids or len(user_ids) != 2:
                return JsonResponse({"error": "Two user IDs are required"}, status=400)

            user_id_1, user_id_2 = user_ids
            if await sync_to_async(Dialog.dialog_exists)(user_id_1, user_id_2):
                return JsonResponse({"error": "Dialog already exists between these users"}, status=400)

            dialog = await Dialog.create_dialog(user_id_1, user_id_2)

            for user_id in user_ids:
                try:
                    await update_list_dialogs_for_target_user(user_id)
                except Exception as e:
                    print(e)

            return Response({"dialog_id": dialog.id}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    else:
        return Response({"error": "Method not allowed"}, status=405)


@api_view(['DELETE'])
async def delete_dialog(request, dialog_id, user_id):
    if request.method != 'DELETE':
        return Response({"error": "Method not allowed"}, status=405)

    try:
        user_dialog = await UserDialog.get_dialog_by_id(user_id=user_id, dialog_id=dialog_id)
        print(user_dialog)

        self_dialog = await UserDialog.objects.aget(user_id=user_id, dialog_id=dialog_id)
        if self_dialog:
            print(12321321)
            companion_dialog = await UserDialog.get_companion_dialog_by_id(dialog_id, user_id)
            print(companion_dialog)
            self_dialog.is_deleted = True
            companion_dialog.is_deleted = True
            await sync_to_async(self_dialog.save)()
            await sync_to_async(companion_dialog.save)()

            dialog = await Dialog.objects.aget(pk=self_dialog.dialog.id)
            dialog.end_date = datetime.datetime.now()
            await sync_to_async(dialog.save)()

            users = [user_id, companion_dialog.user_id]
            for uid in users:
                await update_list_dialogs_for_target_user(uid)

        return Response({"message": "Completed"}, status=200)

    except UserDialog.DoesNotExist:
        return Response({"error": "Dialog not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
async def create_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            message_id = data.get('message_id')
            correction_text = data.get('correction_text')
            description = data.get('description')

            if not user_id or not message_id or not correction_text or not description:
                return JsonResponse({"error": "User ID, message ID, correction text, and description are required"},
                                    status=400)

            feedback = await Feedback.objects.acreate(user_id=user_id,
                                                      message_id=message_id,
                                                      correction_text=correction_text,
                                                      description=description)
            return Response({"feedback_id": feedback.id}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    else:
        return Response({"error": "Method not allowed"}, status=405)


@api_view(['POST'])
async def create_complaint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            dialog_id = data.get('dialog_id')
            description = data.get('description')

            if not user_id or not dialog_id or not description:
                return Response({"error": "User ID, dialog ID, and description are required"}, status=400)

            complaint = await Complaint.objects.acreate(user_id=user_id, dialog_id=dialog_id, description=description)
            return Response({"complaint_id": complaint.id}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    else:
        return Response({"error": "Method not allowed"}, status=405)


def admin_required(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        async with httpx.AsyncClient() as client:
            print(request.headers)
            response = await client.get(f'{os.getenv("gate_way_url")}admin_service/is_admin/',
                                        headers=request.headers)
            if response.status_code != 200:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            return await func(request, *args, **kwargs)

    return wrapper


@api_view(['GET'])
@authentication_classes([])
@admin_required
async def get_statistic_users(request, user_id):
    if request.method == 'GET':
        try:
            count_dialogs_all = await sync_to_async(UserDialog.objects.filter)(Q(user_id=user_id))
            count_dialogs_active = await sync_to_async(count_dialogs_all.filter)(
                Q(user_id=user_id) & ~Q(is_deleted=False))
            count_dialogs_all = await sync_to_async(count_dialogs_all.count)()
            count_dialogs_active = await sync_to_async(count_dialogs_active.count)()

            complaint_count = await sync_to_async(Complaint.objects.filter)(user_id=user_id)
            complaint_count = await sync_to_async(complaint_count.count)()
            complaint_with_answer_count = await sync_to_async(Complaint.objects.filter)(~Q(admin_id=None))
            complaint_with_answer_count = await sync_to_async(complaint_with_answer_count.count)()

            feedback_count = await sync_to_async(Feedback.objects.filter)(user_id=user_id)
            feedback_count = await sync_to_async(feedback_count.count)()

            msg = {
                'count_dialogs_all': count_dialogs_all if count_dialogs_all else 0,
                'count_dialogs_active': count_dialogs_active if count_dialogs_active else 0,
                'complaint_count': complaint_count if complaint_count else 0,
                'complaint_with_answer_count': complaint_with_answer_count if complaint_with_answer_count else 0,
                'feedback_count': feedback_count if feedback_count else 0,
            }

            return Response({'data': msg}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)


@api_view(['GET'])
@authentication_classes([])
async def get_complaints(request, page_number=1, page_size=20,
                         is_answer='false'):  # weil es keine False, True in JS gibt
    try:
        offset = (page_number - 1) * page_size
        complaints = await sync_to_async(Complaint.objects.order_by('created_at').all)() if is_answer == 'false' else \
            await sync_to_async(Complaint.objects.order_by('created_at').filter)(
                ~Q(admin_id=None) & ~Q(resolution=None)
            )
        complaints = await sync_to_async(list)(complaints)
        complaints = complaints[offset:offset + page_size]
        serializer = ComplaintSerializer(complaints, many=True)
        serializer_data = await sync_to_async(serializer.to_representation)(complaints)
        return Response(serializer_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([])
async def get_complaints_by_user_id(request, user_id,
                         is_answer='false'):  # weil es keine False, True in JS gibt
    try:
        complaints = await sync_to_async(Complaint.objects.order_by('created_at').filter)(Q(user_id=user_id)) if is_answer == 'false' else \
            await sync_to_async(Complaint.objects.order_by('created_at').filter)(
                Q(user_id=user_id) & ~Q(admin_id=None)
            )
        complaints = await sync_to_async(list)(complaints)
        serializer = ComplaintSerializer(complaints, many=True)
        serializer_data = await sync_to_async(serializer.to_representation)(complaints)
        return Response(serializer_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([])
async def get_details_dialogs(request, dialog_id):
    try:
        dialog = await Dialog.objects.aget(pk=dialog_id)
        serializer = DialogSerializer(dialog)
        serializer_data = await sync_to_async(serializer.to_representation)(dialog)
        user_dialogs = await sync_to_async(UserDialog.objects.filter)(dialog_id=dialog_id)
        user_dialogs = await sync_to_async(list)(user_dialogs)
        users = await sync_to_async(list)()

        async with httpx.AsyncClient() as client:
            for user_dialog in user_dialogs:
                result = await client.get(
                    f'{os.getenv("gate_way_url")}user_service/get_user_by_id/{str(user_dialog.user_id)}/',
                    headers=request.headers)
                users.append(result.json())
        return Response({'dialog': serializer_data, 'users': users}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([])
async def get_list_dialogs_for_admin(request_id, user_id):
    try:
        dialogs = await sync_to_async(UserDialog.objects.filter)(user_id=user_id)
        dialogs = await sync_to_async(list)(dialogs)
        serializer = UserDialogSerializer(dialogs, many=True)
        serializer_data = await sync_to_async(serializer.to_representation)(dialogs)
        return Response(serializer_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
async def set_resolution_on_complaint(request, complaint_id):
    try:
        complaint = await Complaint.objects.aget(id=complaint_id)
    except Complaint.DoesNotExist:
        return Response({"error": "Complaint not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ResolutionSerializer(data=request.data)
    if serializer.is_valid():
        complaint.resolution = serializer.validated_data['resolution']
        complaint.status = 'done'
        await sync_to_async(complaint.save)()
        return Response({"message": "Resolution set successfully"}, status=status.HTTP_200_OK)
    else:
        print()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([])
async def get_list_messages_for_admin(request, dialog_id):
    try:
        queryset = await sync_to_async(Message.objects.filter)(Q(dialog_id=dialog_id) & Q(is_deleted=False))
        messages = queryset.order_by('send_date')
        messages = await sync_to_async(list)(messages)

        user_dialogs = await sync_to_async(UserDialog.objects.filter)(dialog_id=dialog_id)
        user_dialogs = await sync_to_async(list)(user_dialogs)
        users = await sync_to_async(list)()


        async with httpx.AsyncClient() as client:
            for user_dialog in user_dialogs:
                result = await client.get(
                    f'{os.getenv("gate_way_url")}user_service/get_user_by_id/{user_dialog.user_id}/',
                    headers=request.headers)
                users.append(result.json())

        serializer = MessageSerializer(messages, many=True)
        serializer_data = await sync_to_async(serializer.to_representation)(messages)
        return Response({'messages': serializer_data, 'users': users}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
