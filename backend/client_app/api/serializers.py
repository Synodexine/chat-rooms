from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Client, Settings, Department
from chat.api.serializers import PermissionSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


class ClientSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')
    permission_level = PermissionSerializer()
    full_prefix = serializers.SerializerMethodField('get_prefix')
    department = serializers.SerializerMethodField('get_department')

    class Meta:
        model = Client
        fields = [
            'username',
            'permission_level',
            'department',
            'full_prefix',
        ]

    def get_username(self, instance):
        return instance.user.username

    def get_prefix(self, instance):
        settings = Settings.objects.get(client=instance)
        return f'[{instance.department.name}][{settings.prefix}]'

    def get_department(self, instance):
        dep = instance.department.name
        return dep
