import os
from datetime import datetime
from functools import wraps
import httpx
from asgiref.sync import sync_to_async
from adrf.decorators import api_view
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from main.models import User, Language, UserLanguages
from django.db.models import Q
from main.serializer import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, LanguageSerializer, \
    UserLanguagesSerializer

load_dotenv()


async def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(access)}


@api_view(['POST'])
async def create_user(request):
    data = request.data.copy()

    print(data)

    serializer = UserRegistrationSerializer(data=data)
    if not await sync_to_async(serializer.is_valid)():
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = await sync_to_async(serializer.save)()
    token = await get_tokens_for_user(user)
    return Response(token, status=status.HTTP_201_CREATED)


@api_view(['POST'])
async def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if not await sync_to_async(serializer.is_valid)():
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data['user']
    token = await get_tokens_for_user(user)
    return Response(token, status=status.HTTP_200_OK)


@api_view(['GET'])
async def get_profile(request):
    sync_user_serializer = sync_to_async(UserSerializer)
    serializer = await sync_user_serializer(request.user, many=False)
    to_representation_async = sync_to_async(serializer.to_representation)
    data = await to_representation_async(serializer.instance)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
async def update_profile(request):
    try:
        user_instance = request.user
        serializer = UserSerializer(user_instance, data=request.data, partial=True)

        if await sync_to_async(serializer.is_valid)():
            if 'file' in request.FILES:
                print(1)
                user_instance.photo = request.FILES['file']
                await sync_to_async(user_instance.save)()
            else:
                await sync_to_async(serializer.save)()

            to_representation_async = sync_to_async(serializer.to_representation)
            data = await to_representation_async(serializer.instance)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([])
async def get_user_by_id(request, *args, **kwargs):
    try:
        user = await User.objects.aget(pk=kwargs['user_id'])
        serializer = UserSerializer(user)
        to_representation_async = sync_to_async(serializer.to_representation)
        data = await to_representation_async(serializer.instance)
        print(data)
        return Response(data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
async def get_languages(request):
    languages = await sync_to_async(list)(Language.objects.all())
    serializer = LanguageSerializer(languages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])  # hier gibt es keine POST, weil wir einfach USER model upd
async def add_language(request):
    print(request.data)
    language = request.data['user_language']['language']
    proficiency_level = request.data.get('user_language', {}).get('proficiency_level')
    is_learning = request.data.get('user_language', {}).get('is_learning') or False

    try:
        language = await Language.objects.aget(pk=language['id'])
        user_language = await UserLanguages.objects.acreate(language=language,
                                                            user=request.user,
                                                            proficiency_level=proficiency_level,
                                                            is_learning=is_learning)
        serializer = UserLanguagesSerializer(user_language)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Language.DoesNotExist:
        return Response({"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
async def delete_language(request, language_id):
    try:
        language = await Language.objects.aget(pk=language_id)
        user_language = await UserLanguages.objects.aget(language=language, user=request.user)
        await sync_to_async(user_language.delete)()
        serializer = UserSerializer(request.user)
        serialized_data = await sync_to_async(serializer.to_representation)(request.user)

        return Response(serialized_data, status=status.HTTP_202_ACCEPTED)
    except Language.DoesNotExist:
        return Response({"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
async def get_suitable_users(request):
    users_suitable_query = await sync_to_async(User.func.get_list_suitable_users)(request.user)
    users_suitable = await sync_to_async(list)(users_suitable_query)
    serializer = UserSerializer(users_suitable, many=True)
    serialized_data = await sync_to_async(serializer.to_representation)(users_suitable)
    """[
        {
            "id": 2,
            "username": "nikakoy_",
            "email": "email@gmail.com",
            "gender": null,
            "first_name": "last_name",
            "last_name": "Katya",
            "status": "online",
            "last_active_date": "2024-03-07T22:48:27.909086Z",
            "registration_date": "2024-03-07T22:48:27.909086Z",
            "photo": "/media/user_photos/das-gewisse-etwas_ZueFtlr.jpg",
            "phone": "123123213",
            "birth_date": "2000-12-10",
            "languages": [
                {
                    "id": 3,
                    "language": {
                        "id": 2,
                        "title": "Germany"
                    },
                    "proficiency_level": "С1",
                    "is_learning": true
                },
                {
                    "id": 1,
                    "language": {
                        "id": 1,
                        "title": "English"
                    },
                    "proficiency_level": "A1",
                    "is_learning": true
                }
            ]
        }
    ]
    
    Beispiel 
    """
    return Response(serialized_data, status=status.HTTP_200_OK)


def admin_required(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        print(request.headers)
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{os.environ.get("gate_way_url")}admin_service/is_admin/',
                                        headers=request.headers)
            if response.status_code != 200:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            return await func(request, *args, **kwargs)

    return wrapper


@api_view(['GET'])
@authentication_classes([])
@admin_required
async def get_list_users_for_admin(request, page_number=1, page_size=20):
    try:
        offset = (page_number - 1) * page_size
        users = await sync_to_async(User.objects.all)()
        users = await sync_to_async(list)(users)
        users = users[offset:offset + page_size]
        serializer = UserSerializer(users, many=True)
        serialized_data = await sync_to_async(serializer.to_representation)(users)
        return Response(serialized_data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f'Error in get_list_users_for_admin: {e}')
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([])
@admin_required
async def get_user_for_admin(request, username):
    try:
        users = await sync_to_async(User.objects.filter)(
            Q(username__icontains=username)
            |
            Q(email__icontains=username)
        )
        users = await sync_to_async(list)(users)
        serializer = UserSerializer(users, many=True)
        serialized_data = await sync_to_async(serializer.to_representation)(users)
        return Response(serialized_data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@authentication_classes([])
async def update_user_status_for_admin(request, user_id):
    try:
        user = await User.objects.aget(pk=user_id)
        user.is_active = not user.is_active
        await sync_to_async(user.save)()
        return Response({'success': True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



