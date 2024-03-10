from rest_framework import serializers
from .models import Service, Version


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    versions = VersionSerializer(many=True, read_only=True, source='version_set')

    class Meta:
        model = Service
        fields = '__all__'


