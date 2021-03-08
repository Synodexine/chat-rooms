import ast

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RoomSerializer, DeleteRoomSerializer
from ..models import Room


class RoomListViewSet(GenericViewSet, ListModelMixin):
    serializer_class = RoomSerializer
    queryset = Room.objects.order_by('permission_level')
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]


@api_view(http_method_names=['POST'])
def delete_room(request, *args, **kwargs):
    if request.user.client.permission_level >= 4:
        data = ast.literal_eval(bytes.decode(request.body, 'UTF-8'))
        serializer = DeleteRoomSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
    return Response({'success': 'deleted'}, status=204)
