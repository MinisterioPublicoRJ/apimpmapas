from rest_framework import serializers


class AcervoSerializer(serializers.Serializer):
    acervo_qtd = serializers.IntegerField()


class AcervoVariationSerializer(serializers.Serializer):
    acervo_fim = serializers.IntegerField(min_value=0)
    acervo_inicio = serializers.IntegerField(min_value=0)
    variacao = serializers.FloatField()


class AcervoVariationTopNSerializer(serializers.Serializer):
    cod_orgao = serializers.IntegerField()
    nm_orgao = serializers.CharField()
    acervo_fim = serializers.IntegerField(min_value=0)
    acervo_inicio = serializers.IntegerField(min_value=0)
    variacao = serializers.FloatField()


class OutliersSerializer(serializers.Serializer):
    cod_atribuicao = serializers.IntegerField()
    minimo = serializers.IntegerField(min_value=0)
    maximo = serializers.IntegerField(min_value=0)
    media = serializers.FloatField()
    primeiro_quartil = serializers.FloatField()
    mediana = serializers.FloatField()
    terceiro_quartil = serializers.FloatField()
    iqr = serializers.FloatField()
    lout = serializers.FloatField()
    hout = serializers.FloatField()


class SaidasSerializer(serializers.Serializer):
    saidas = serializers.IntegerField(min_value=0)
    id_orgao = serializers.IntegerField()
    cod_pct = serializers.IntegerField()
    percent_rank = serializers.FloatField()
    dt_calculo = serializers.DateTimeField()
