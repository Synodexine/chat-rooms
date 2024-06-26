from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Channels API",
        default_version='v1',
        description="LSD"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


api_patterns = [
    path('accounts/', include('client_app.api.urls')),
    path('chat/', include('chat.api.urls'))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((api_patterns, 'api'), namespace='api')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('chat/', include('chat.urls')),
]
