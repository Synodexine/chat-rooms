import ast
from django.contrib.auth.models import User

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from .serializers import UserSerializer, ClientSerializer
from ..models import Client, Department, Settings


class RegistrationView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(username=serializer.data['username'])
            user.set_password(raw_password=serializer.data['password'])
            user.save()
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token}, status=201)
        else:
            return Response(serializer.errors, status=400)


class UserInfoView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return Response({'error': 'No client for this user. Im sorry :('}, status=404)
        serializer = ClientSerializer(instance=client)
        return Response(serializer.data, status=200)


@api_view(http_method_names=['POST'])
def change_user_prefix(request, *args, **kwargs):
    settings = Settings.objects.get(client=request.user.client)
    data = ast.literal_eval(bytes.decode(request.body, 'UTF-8'))
    settings.prefix = data['prefix']
    settings.save()
    return Response({'success': 'changed'}, status=200)
