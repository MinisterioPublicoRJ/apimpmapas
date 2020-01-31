from rest_framework import serializers


class AcervoSerializer(serializers.Serializer):
    acervo_qtd = serializers.IntegerField()


class AcervoVariationSerializer(serializers.Serializer):
    acervo_fim = serializers.IntegerField(min_value=0)
    acervo_inicio = serializers.IntegerField(min_value=0)
    variacao = serializers.FloatField()


class AcervoVariationTopNSerializer(serializers.Serializer):
    acervo_fim = serializers.IntegerField(min_value=0)
    acervo_inicio = serializers.IntegerField(min_value=0)
    variacao = serializers.FloatField()
    cod_orgao = serializers.IntegerField()


class OutliersSerializer(serializers.Serializer):
    pacote_atribuicao = serializers.CharField()
    minimo = serializers.IntegerField(min_value=0)
    maximo = serializers.IntegerField()
    media = serializers.FloatField()
    primeiro_quartil = serializers.FloatField()
    mediana = serializers.FloatField()
    terceiro_quartil = serializers.FloatField()
    iqr = serializers.FloatField()
    lout = serializers.FloatField()
    hout = serializers.FloatField()
