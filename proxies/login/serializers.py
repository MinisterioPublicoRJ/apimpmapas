from django.conf import settings
from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from login.sca import authenticate as sca_authenticate
from proxies.login.tokens import SCARefreshToken, TokenDoesNotHaveRoleException


class SCAJWTTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        sca_auth = sca_authenticate(
            attrs["username"],
            attrs["password"],
            roles=(settings.PROXIES_PLACAS_ROLE,),
        )
        if not sca_auth["logged_in"]:
            raise PermissionDenied

        refresh = SCARefreshToken(username=attrs["username"])

        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class SCAJWTRefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            refresh = SCARefreshToken(token=attrs["refresh"])
        except TokenDoesNotHaveRoleException:
            raise serializers.ValidationError(
                "Token não possui ROLE para esse endpoint"
            )

        return {"access": str(refresh.access_token)}
