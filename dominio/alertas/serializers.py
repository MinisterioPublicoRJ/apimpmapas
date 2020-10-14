from rest_framework import serializers


class AlertasListaSerializer(serializers.Serializer):
    id_alerta = serializers.CharField()
    sigla = serializers.CharField()
    descricao = serializers.CharField()
    doc_dk = serializers.IntegerField()
    num_doc = serializers.CharField()
    num_ext = serializers.CharField()
    etiqueta = serializers.CharField()
    classe_doc = serializers.CharField()
    data_alerta = serializers.DateTimeField()
    orgao = serializers.IntegerField()
    classe_hier = serializers.CharField()
    dias_passados = serializers.IntegerField()


class AlertasResumoSerializer(serializers.Serializer):
    sigla = serializers.CharField()
    descricao = serializers.CharField()
    orgao = serializers.IntegerField()
    count = serializers.IntegerField()


class AlertasComprasSerializer(serializers.Serializer):
    sigla = serializers.CharField()
    contrato = serializers.CharField()  # Talvez integer? Muito grande?
    iditem = serializers.IntegerField()
    contrato_iditem = serializers.CharField()
    item = serializers.CharField()


class IdentificadorAlertaSerializer(serializers.Serializer):
    alerta_id = serializers.CharField()


class AlertaOverlayPrescricaoSerializer(serializers.Serializer):
    tipo_penal = serializers.CharField()
    nm_investigado = serializers.CharField()
    max_pena = serializers.FloatField()
    delitos_multiplicadores = serializers.CharField()
    fator_pena = serializers.FloatField()
    max_pena_fatorado = serializers.FloatField()
    dt_inicio_prescricao = serializers.CharField()
    dt_fim_prescricao = serializers.CharField()
    adpr_chave = serializers.CharField()
