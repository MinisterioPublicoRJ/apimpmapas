from rest_framework import serializers


class AcervoSerializer(serializers.Serializer):
    acervo_qtd = serializers.IntegerField()


class AcervoVariationSerializer(serializers.Serializer):
    acervo_fim = serializers.IntegerField(min_value=0)
    acervo_inicio = serializers.IntegerField(min_value=0)
    variacao = serializers.FloatField()
