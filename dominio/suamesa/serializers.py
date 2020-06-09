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
    variacao_documentos_distintos = serializers.FloatField()
    variacao_aberturas_vista = serializers.FloatField()
    variacao_aproveitamentos = serializers.FloatField()
    variacao_instaurados = serializers.FloatField()


class SuaMesaDetalheOrgaoSerializer(serializers.Serializer):
    tipo_detalhe = serializers.CharField()
    intervalo = serializers.IntegerField()
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


class SuaMesaDetalheTopNSerializer(serializers.Serializer):
    nm_orgao = serializers.CharField()
    valor = serializers.FloatField()


class SuaMesaDetalheAISPSerializer(serializers.Serializer):
    acervo_inicio = serializers.IntegerField(min_value=0)
    acervo_fim = serializers.IntegerField(min_value=0)
    variacao_acervo = serializers.FloatField()
    aisp_nomes = serializers.CharField()


class SuaMesaDetalheAndamentosSerializer(serializers.Serializer):
    orgao_id = serializers.IntegerField()
    tipo_detalhe = serializers.CharField
    intervalo = serializers.IntegerField()
    nm_orgao = serializers.CharField()
    cod_pct = serializers.IntegerField()
    nr_andamentos_atual = serializers.IntegerField(min_value=0)
    nr_andamentos_anterior = serializers.IntegerField(min_value=0)
    variacao_andamentos = serializers.FloatField()
