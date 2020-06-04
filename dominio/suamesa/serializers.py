from rest_framework import serializers


class SuaMesaDetalheCPFSerializer(serializers.Serializer):
    tipo_detalhe = serializers.CharField()
    intervalo = serializers.IntegerField()
    orgao_id = serializers.IntegerField()
    cpf = serializers.CharField()
    nr_documentos_distintos_atual = serializers.IntegerField(min_value=0)
    nr_aberturas_vista_atual = serializers.IntegerField(min_value=0)
    nr_aproveitamentos_atual = serializers.IntegerField(min_value=0)
    nr_instaurados_atual = serializers.IntegerField(min_value=0)
    nr_documentos_distintos_anterior = serializers.IntegerField(min_value=0)
    nr_aberturas_vista_anterior = serializers.IntegerField(min_value=0)
    nr_aproveitamentos_anterior = serializers.IntegerField(min_value=0)
    nr_instaurados_anterior = serializers.IntegerField(min_value=0)
    variacao_nr_documentos_distintos = serializers.FloatField()
    variacao_nr_aberturas_vista = serializers.FloatField()
    variacao_nr_aproveitamentos = serializers.FloatField()
    variacao_nr_instaurados = serializers.FloatField()


class SuaMesaDetalheTopNSerializer(serializers.Serializer):
    nm_orgao = serializers.CharField()
    valor = serializers.FloatField()