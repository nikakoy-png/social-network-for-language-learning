from django.shortcuts import render
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from adrf.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from main.models import User, Language, UserLanguages
from main.serializer import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, LanguageSerializer, \
    UserLanguagesSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


async def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(access)}


@api_view(['POST'])
async def create_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if not await sync_to_async(serializer.is_valid)():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = await sync_to_async(serializer.save)()
    token = await get_tokens_for_user(user)
    return Response(token, status=status.HTTP_201_CREATED)


@api_view(['POST'])
async def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if not await sync_to_async(serializer.is_valid)():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data['user']
    token = await get_tokens_for_user(user)
    return Response(token, status=status.HTTP_200_OK)


@api_view(['GET'])
async def get_languages(request):
    languages = await sync_to_async(list)(Language.objects.all())
    serializer = LanguageSerializer(languages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH']) # hier gibt es keine POST, weil wir einfach USER model upd
async def add_language(request):
    language_id = request.data.get('language_id')
    try:
        language = await Language.objects.aget(pk=language_id)
        await sync_to_async(request.user.languages.add)(language)
        await sync_to_async(request.user.save)()
        serializer = LanguageSerializer(language)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Language.DoesNotExist:
        return Response({"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
async def delete_language(request):
    language_id = request.data.get('language_id')
    try:
        language = await Language.objects.aget(pk=language_id)
        await sync_to_async(request.user.languages.remove)(language)
        await sync_to_async(request.user.save)()

        user_language = await sync_to_async(UserLanguages.objects.get)(user=request.user)
        serializer = UserLanguagesSerializer(user_language)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    except Language.DoesNotExist:
        return Response({"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
async def get_suitable_users(request):
    users_suitable_query = await sync_to_async(User.func.get_list_suitable_users)(request.user)
    users_suitable = await sync_to_async(list)(users_suitable_query)
    serializer = UserSerializer(users_suitable, many=True)
    serialized_data = await sync_to_async(serializer.to_representation)(users_suitable)
    return Response(serialized_data, status=status.HTTP_200_OK)



