from django.urls import path

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .views import RegistrationView, UserInfoView


router = routers.DefaultRouter()
router.register(r'registration', RegistrationView, 'registration')

urlpatterns = [
    path('obtain_token/', obtain_jwt_token),
    path('refresh_token/', refresh_jwt_token),
    path('verify_token/', verify_jwt_token),
    path('get-user-info/', UserInfoView.as_view())
] + router.urls
