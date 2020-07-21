from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

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
            token_obj = AccessToken(token=attrs["token"])
            payload = token_obj.payload
        except TokenError as e:
            raise serializers.ValidationError("{!r}".format(e))

        return {"payload": payload}
