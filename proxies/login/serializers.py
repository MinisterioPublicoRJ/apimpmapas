from django.conf import settings
from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from login.sca import authenticate as sca_authenticate
from proxies.login.tokens import SCARefreshToken


class SCAJWTTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        sca_auth = sca_authenticate(
            attrs["username"],
            attrs["password"],
            roles=(settings.PROXIES_PLACAS_ROLE,),
        )
        if not sca_auth["logged_in"]:
            raise PermissionDenied

        refresh = SCARefreshToken()

        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class SCAJWTRefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = SCARefreshToken(attrs["refresh"])
        if settings.PROXIES_PLACAS_ROLE not in refresh.payload["roles"]:
            raise serializers.ValidationError(
                "Token não possui ROLE para esse endpoint"
            )

        refresh.set_roles()
        return {"access": str(refresh.access_token)}
