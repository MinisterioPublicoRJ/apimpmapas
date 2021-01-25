from django.conf import settings
from rest_framework import serializers


class SolrPlacasSerializer(serializers.Serializer):
    dt_format = "%Y-%m-%dT%H:%M:%S"

    placa = serializers.CharField()
    dt_inicio = serializers.DateTimeField(format=dt_format)
    dt_fim = serializers.DateTimeField(format=dt_format)
    start = serializers.IntegerField(min_value=0)
    rows = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        if attrs["rows"] > settings.PLACAS_SOLR_MAX_ROWS:
            raise serializers.ValidationError(
                "Limite máximo de linhas excedido:"
                f" max={settings.PLACAS_SOLR_MAX_ROWS}"
            )

        dt_inicio = attrs["dt_inicio"].strftime(self.dt_format)
        dt_fim = attrs["dt_fim"].strftime(self.dt_format)
        query = (
            f"datapassagem:[{dt_inicio}Z TO {dt_fim}Z]"
            f" AND placa:{attrs['placa']}"
        )

        return {"query": query, "start": attrs["start"], "rows": attrs["rows"]}


class SolrCadUnicoSerializer(serializers.Serializer):
    f_q = serializers.CharField()
    start = serializers.IntegerField(min_value=0)
    rows = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        if attrs["rows"] > settings.CADUNICO_SOLR_MAX_ROWS:
            raise serializers.ValidationError(
                "Limite máximo de linhas excedido:"
                f" max={settings.CADUNICO_SOLR_MAX_ROWS}"
            )

        return attrs
