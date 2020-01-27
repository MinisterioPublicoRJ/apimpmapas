from rest_framework import serializers


class AcervoSerializer(serializers.Serializer):
    acervo_qtd = serializers.IntegerField()
