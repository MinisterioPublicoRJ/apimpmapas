from rest_framework import serializers


class MetricsDetalheDocumentoOrgaoCPFSerializer(serializers.Serializer):
    tipo_detalhe = serializers.CharField()
    intervalo = serializers.CharField()
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
    variacao_documentos_distintos = serializers.FloatField()
    variacao_aberturas_vista = serializers.FloatField()
    variacao_aproveitamentos = serializers.FloatField()
    variacao_instaurados = serializers.FloatField()


class MetricsDetalheDocumentoOrgaoSerializer(serializers.Serializer):
    tipo_detalhe = serializers.CharField()
    intervalo = serializers.CharField()
    nm_orgao = serializers.CharField()
    cod_pacote = serializers.IntegerField()
    orgao_id = serializers.IntegerField()
    nr_documentos_distintos_atual = serializers.IntegerField(min_value=0)
    nr_aberturas_vista_atual = serializers.IntegerField(min_value=0)
    nr_aproveitamentos_atual = serializers.IntegerField(min_value=0)
    nr_instaurados_atual = serializers.IntegerField(min_value=0)
    acervo_anterior = serializers.IntegerField(min_value=0)
    acervo_atual = serializers.IntegerField(min_value=0)
    variacao_acervo = serializers.FloatField()
    nr_documentos_distintos_anterior = serializers.IntegerField(min_value=0)
    nr_aberturas_vista_anterior = serializers.IntegerField(min_value=0)
    nr_aproveitamentos_anterior = serializers.IntegerField(min_value=0)
    nr_instaurados_anterior = serializers.IntegerField(min_value=0)
    variacao_documentos_distintos = serializers.FloatField()
    variacao_aberturas_vista = serializers.FloatField()
    variacao_aproveitamentos = serializers.FloatField()
    variacao_instaurados = serializers.FloatField()


class RankingSerializer(serializers.Serializer):
    nm_orgao = serializers.CharField()
    valor = serializers.IntegerField()


class RankingFloatSerializer(serializers.Serializer):
    nm_orgao = serializers.CharField()
    valor = serializers.FloatField()


class RankingPercentageSerializer(serializers.Serializer):
    nm_orgao = serializers.CharField()
    valor_percentual = serializers.FloatField()


class SuaMesaDetalheAISPSerializer(serializers.Serializer):
    acervo_inicio = serializers.IntegerField(min_value=0)
    acervo_fim = serializers.IntegerField(min_value=0)
    variacao_acervo = serializers.FloatField()
    aisp_nomes = serializers.CharField()


class SuaMesaDetalheTutelaProcessosSerializer(serializers.Serializer):
    orgao_id = serializers.IntegerField()
    nm_orgao = serializers.CharField()
    nr_acoes_ultimos_60_dias = serializers.IntegerField(min_value=0)
    variacao_12_meses = serializers.FloatField()
    nr_acoes_ultimos_30_dias = serializers.IntegerField(min_value=0)
