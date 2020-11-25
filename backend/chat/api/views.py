from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import RoomSerializer
from ..models import Room


class RoomListViewSet(GenericViewSet, ListModelMixin):
    serializer_class = RoomSerializer
    queryset = Room.objects.order_by('permission_level')
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
