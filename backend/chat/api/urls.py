from django.urls import path

from rest_framework import routers

from .views import RoomListViewSet


router = routers.DefaultRouter()
router.register(r'get-rooms', RoomListViewSet, 'rooms-list')

urlpatterns = [

] + router.urls
