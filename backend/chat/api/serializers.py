from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Room
from client_app.enums import PermissionsDict


class PermissionSerializer(serializers.Serializer):
    level_id = serializers.IntegerField()
    level_name = serializers.CharField(max_length=64, read_only=True)

    def to_representation(self, instance):
        self.level_id = instance
        self.level_name = PermissionsDict[instance]
        return super().to_representation(self)


class RoomSerializer(serializers.ModelSerializer):
    permission_level = serializers.SerializerMethodField(method_name='permission_level_get')

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'capacity',
            'users_online',
            'permission_level',
        ]

    def permission_level_get(self, instance):
        return {
            'level_id': instance.permission_level,
            'level_name': PermissionsDict[instance.permission_level],
        }


class DeleteRoomSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        try:
            room = Room.objects.get(id=validated_data['room_id'])
            room.delete()
            return room
        except Room.DoesNotExist:
            raise ValidationError({'room_id': 'does not exist'}, code=404)
