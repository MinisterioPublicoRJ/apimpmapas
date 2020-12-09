from rest_framework import serializers


class AlertasListaSerializer(serializers.Serializer):
    id_alerta = serializers.CharField()
    sigla = serializers.CharField()
    doc_dk = serializers.IntegerField()
    num_doc = serializers.CharField()
    data_alerta = serializers.DateTimeField(format="%Y-%m-%d")
    orgao = serializers.IntegerField()
    dias_passados = serializers.IntegerField()
    descricao = serializers.CharField()
    classe_hierarquia = serializers.CharField()
    num_externo = serializers.CharField()


class AlertasResumoSerializer(serializers.Serializer):
    sigla = serializers.CharField()
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
    dt_inicio_prescricao = serializers.DateTimeField(format="%Y-%m-%d")
    dt_fim_prescricao = serializers.DateTimeField(format="%Y-%m-%d")
    adpr_chave = serializers.CharField()


class DetalheAlertaSerializer(serializers.Serializer):
    contratacao = serializers.CharField()
    data_contratacao = serializers.DateTimeField(format="%Y-%m-%d")
    item_contratado = serializers.CharField()
    var_perc = serializers.SerializerMethodField()

    def get_var_perc(self, obj):
        return str(obj.get("var_perc", "")).replace(".", ",")
