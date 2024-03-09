from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from main.models import User, Language, UserLanguages, LevelLanguageENUM
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from passlib.hash import pbkdf2_sha256
from user_service.settings import SECRET_KEY


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    photo = serializers.ImageField(write_only=True)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'password',
                  'password_confirm',
                  'phone',
                  'gender',
                  'photo',
                  'birth_date'
                  ]
        extra_kwargs = {'password': {'write_only': True}, 'photo': {'write_only': True}}

    def create(self, validated_data):
        password = self.validated_data.pop('password')
        hashed_password = pbkdf2_sha256.hash(password, salt=SECRET_KEY.encode('utf-8'))
        return User.objects.create(password=hashed_password, **self.validated_data)

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, write_only=True, required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = pbkdf2_sha256.hash(attrs.get('password'), salt=SECRET_KEY.encode('utf-8'))

        user = User.objects.get(username=username, password=password)
        if user is None:
            raise ValidationError('Invalid username/password')

        refresh = RefreshToken.for_user(user)
        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = user

        return data


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class UserLanguagesSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(many=False)
    proficiency_level = serializers.ChoiceField(choices=LevelLanguageENUM.choices)
    is_learning = serializers.BooleanField()

    class Meta:
        model = UserLanguages
        fields = ['id', 'language', 'proficiency_level', 'is_learning']


class UserSerializer(serializers.ModelSerializer):
    languages = UserLanguagesSerializer(source='userlanguages_set', many=True)
    photo = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'gender',
                  'first_name',
                  'last_name',
                  'status',
                  'last_active_date',
                  'registration_date',
                  'photo',
                  'phone',
                  'birth_date',
                  'languages',
                  )
