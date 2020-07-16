from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

from login.sca import authenticate


class SCARefreshToken(RefreshToken):
    def set_roles(self):
        self.payload["roles"] = (settings.PROXIES_PLACAS_ROLE,)


class SCAJWTTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        sca_auth = authenticate(
            attrs["username"],
            attrs["password"],
            roles=(settings.PROXIES_PLACAS_ROLE,),
        )
        if not sca_auth["logged_in"]:
            raise PermissionDenied

        refresh = SCARefreshToken()
        refresh.set_roles()

        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class SCAJWTRefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = SCARefreshToken(attrs["refresh"])
        if (
            not settings.PROXIES_PLACAS_ROLE
            in refresh.payload["roles"]
        ):
            raise serializers.ValidationError(
                "Token não possui ROLE para esse endpoint"
            )

        refresh.set_roles()
        return {"access": str(refresh.access_token)}
