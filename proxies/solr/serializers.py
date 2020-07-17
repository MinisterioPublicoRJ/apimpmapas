from rest_framework import serializers

from proxies.login.tokens import SCAAccessToken


class SolrPlacasSerializer(serializers.Serializer):
    jwt = serializers.CharField()
    query = serializers.CharField()
    start = serializers.IntegerField()
    rows = serializers.IntegerField()

    def validate(self, attrs):
        token = SCAAccessToken(attrs["jwt"])
        return attrs
