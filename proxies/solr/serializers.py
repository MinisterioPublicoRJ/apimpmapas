from rest_framework import serializers


class SolrPlacasSerializer(serializers.Serializer):
    query = serializers.CharField()
    start = serializers.IntegerField()
    rows = serializers.IntegerField()
