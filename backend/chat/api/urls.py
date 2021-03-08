from django.urls import path

from rest_framework import routers

from .views import RoomListViewSet, delete_room


router = routers.DefaultRouter()
router.register(r'get-rooms', RoomListViewSet, 'rooms-list')

urlpatterns = [
    path('delete-room/', delete_room, name='delete-room'),
] + router.urls
