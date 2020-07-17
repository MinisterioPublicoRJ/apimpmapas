from rest_framework import serializers

from proxies.login.tokens import SCAAccessToken


class SolrPlacasSerializer(serializers.Serializer):
    jwt = serializers.CharField()
    query = serializers.CharField()
    start = serializers.IntegerField()
    rows = serializers.IntegerField()

    def validate(self, attrs):
        token_obj = SCAAccessToken(token=attrs["jwt"])
        attrs.update(token_obj.payload)
        return attrs
