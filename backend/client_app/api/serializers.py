from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Client
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

    class Meta:
        model = Client
        fields = [
            'username',
            'permission_level'
        ]

    def get_username(self, instance):
        return instance.user.username
