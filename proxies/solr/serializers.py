from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError

from proxies.login.tokens import SCAAccessToken


class SolrPlacasSerializer(serializers.Serializer):
    jwt = serializers.CharField()
    query = serializers.CharField()
    start = serializers.IntegerField()
    rows = serializers.IntegerField()

    def validate(self, attrs):
        try:
            token_obj = SCAAccessToken(token=attrs["jwt"])
        except TokenError as e:
            raise serializers.ValidationError("{!r}".format(e))

        attrs.update(token_obj.payload)
        return attrs
