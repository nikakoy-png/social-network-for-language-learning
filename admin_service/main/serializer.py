from rest_framework import serializers
from passlib.hash import pbkdf2_sha256
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from admin_service.settings import SECRET_KEY
from main.models import Admin, Performance


class AdminLoginSerializer(serializers.Serializer):
    try:
        username = serializers.CharField(max_length=255, write_only=True, required=True)
        password = serializers.CharField(max_length=255, write_only=True, required=True)

        def validate(self, attrs):
            username = attrs.get('username')
            password = pbkdf2_sha256.hash(attrs.get('password'), salt=SECRET_KEY.encode('utf-8'))

            print(username, password)
            user = Admin.objects.get(username=username, password=password)
            if user is None:
                raise ValidationError('Invalid username/password')

            refresh = RefreshToken.for_user(user)
            data = {}
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['user'] = user

            return data
    except Exception as e:
        print(e)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['password']


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'

