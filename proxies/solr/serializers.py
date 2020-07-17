from rest_framework import serializers


class SolrPlacasSerializer(serializers.Serializer):
    jwt = serializers.CharField()
    query = serializers.CharField()
    start = serializers.IntegerField()
    rows = serializers.IntegerField()
