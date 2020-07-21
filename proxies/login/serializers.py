import jwt
from django.conf import settings
from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from login.sca import authenticate as sca_authenticate
from proxies.login.tokens import SCAAccessToken


class SCATokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        sca_auth = sca_authenticate(
            attrs["username"],
            attrs["password"],
            verify_roles=False,
        )
        if not sca_auth["logged_in"]:
            raise PermissionDenied

        refresh = SCAAccessToken(
            username=attrs["username"],
            roles=sca_auth["permissions"]
        )

        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class SCAPermissionSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            payload = jwt.decode(
                attrs["token"],
                settings.JWT_SECRET,
                algorithm="HS256"
            )
        except jwt.exceptions.InvalidTokenError:
            raise serializers.ValidationError("Token Inválido")

        return {"payload": payload}
