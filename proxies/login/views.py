from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenViewBase

from proxies.login.serializers import SCATokenSerializer


class SCAJSONWebTokenAPIView(TokenViewBase):
    serializer_class = SCATokenSerializer


class SCAJSONWebRefreshTokenAPIView(TokenViewBase):
    serializer_class = TokenRefreshSerializer
