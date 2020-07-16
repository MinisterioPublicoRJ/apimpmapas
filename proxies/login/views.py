from rest_framework_simplejwt.views import TokenViewBase

from proxies.login.serializers import (
    SCAJWTTokenSerializer,
    SCAJWTRefreshTokenSerializer,
)


class SCAJSONWebTokenAPIView(TokenViewBase):
    serializer_class = SCAJWTTokenSerializer


class SCAJSONWebRefreshTokenAPIView(TokenViewBase):
    serializer_class = SCAJWTRefreshTokenSerializer
