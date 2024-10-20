import os

from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from asgiref.sync import sync_to_async
from main.models import Admin, Performance
from main.permissions import IsAdminUser
from main.serializer import AdminSerializer, AdminLoginSerializer, PerformanceSerializer
from adrf.decorators import api_view
import httpx

load_dotenv()


async def get_token_for_admin(admin):
    refresh = RefreshToken.for_user(admin)
    access = AccessToken.for_user(admin)
    return {'refresh': str(refresh), 'access': str(access)}


async def get_admin_object(request):
    try:
        token = request.headers.get('Authorization').split()[1]
        access_token = AccessToken(token)

        user_id = access_token.payload.get('user_id')

        admin = await Admin.objects.aget(pk=user_id)
        return admin
    except Exception as e:
        return None


@api_view(['GET'])
async def get_admin_data(request, admin_id):
    try:
        admin = await Admin.objects.aget(pk=admin_id)
        serializer = AdminSerializer(admin)
        serialized_data = await sync_to_async(serializer.to_representation)(admin)
        return Response(serialized_data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(f'Admin not found! {e}', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
async def login_admin(request):
    try:
        serializer = AdminLoginSerializer(data=request.data)
        if not await sync_to_async(serializer.is_valid)():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        admin = serializer.validated_data['user']
        token = await get_token_for_admin(admin)
        return Response(token, status=status.HTTP_200_OK)
    except Admin.DoesNotExist:
        return Response({'error': 'Admin does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)


@api_view(['GET'])
@permission_classes([IsAdminUser])
async def get_list_users(request, page_number=1, page_size=20):
    try:
        print(324234)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'{os.environ.get('gate_way_url')}user_service/get_list_users/{page_number}/{page_size}/',
                headers=request.headers)
            if response.status_code == 200:
                data = response.json()
                return Response({'data': data}, status=status.HTTP_200_OK)
            return Response({'error': 'Failed to fetch data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
async def is_admin(request):
    try:
        token = request.headers.get('Authorization').split()[1]
        access_token = AccessToken(token)

        user_id = access_token.payload.get('user_id')

        admin = await Admin.objects.aget(pk=user_id)
        return Response({'data': str(True)}, status=status.HTTP_200_OK)
    except (Admin.DoesNotExist, KeyError):
        return Response({'error': 'Admin not found!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
async def get_performances(request, user_id):
    try:
        performances = await sync_to_async(Performance.objects.filter)(user_id=user_id)
        serializer = PerformanceSerializer(performances, many=True)
        serialized_data = await sync_to_async(serializer.to_representation)(performances)
        return Response(serialized_data, status=status.HTTP_200_OK)
    except (Performance.DoesNotExist, KeyError):
        return Response('Performance not found!', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
async def get_count_performances(request, user_id):
    try:
        performances = await sync_to_async(Performance.objects.filter)(user_id=user_id)
        performances_count = await sync_to_async(performances.count)()
        return Response({'count_performances': performances_count}, status=status.HTTP_200_OK)
    except (Performance.DoesNotExist, KeyError):
        return Response({'count_performances': 0}, status=status.HTTP_200_OK)


@api_view(['POST'])
async def add_performance(request):
    try:
        data = request.data.copy()
        admin = await get_admin_object(request)
        if admin is None:
            return Response("Admin not found", status=status.HTTP_400_BAD_REQUEST)
        performance = await sync_to_async(Performance.objects.create)(
            admin=admin,
            **data)
        return Response(PerformanceSerializer(performance).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(str(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
