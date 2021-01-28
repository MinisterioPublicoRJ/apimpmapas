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
    alrt_key = serializers.CharField()
    flag_dispensado = serializers.IntegerField()


class AlertasResumoSerializer(serializers.Serializer):
    sigla = serializers.CharField()
    count = serializers.IntegerField()


class AlertasComprasSerializer(serializers.Serializer):
    sigla = serializers.CharField()
    contrato = serializers.CharField()  # Talvez integer? Muito grande?
    iditem = serializers.IntegerField()
    contrato_iditem = serializers.CharField()
    item = serializers.CharField()
    alrt_key = serializers.CharField()
    flag_dispensado = serializers.IntegerField()


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


class AlertasABR1Serializer(serializers.Serializer):
    alrt_key = serializers.CharField()
    alrt_sigla = serializers.CharField()
    alrt_orgi_orga_dk = serializers.IntegerField()
    abr1_nr_procedimentos = serializers.IntegerField()
    abr1_ano_mes = serializers.CharField()


class AlertasCOMPSerializer(serializers.Serializer):
    alrt_key = serializers.CharField()
    alrt_sigla = serializers.CharField()
    alrt_orgi_orga_dk = serializers.IntegerField()
    comp_contratacao = serializers.CharField()
    comp_item = serializers.CharField()
    comp_id_item = serializers.CharField()
    comp_contrato_iditem = serializers.CharField()


class AlertasISPSSerializer(serializers.Serializer):
    alrt_key = serializers.CharField()
    alrt_sigla = serializers.CharField()
    alrt_orgi_orga_dk = serializers.IntegerField()
    isps_municipio = serializers.CharField()
    isps_indicador = serializers.CharField()
    isps_ano_referencia = serializers.IntegerField()


class AlertasMGPSerializer(serializers.Serializer):
    alrt_key = serializers.CharField()
    alrt_sigla = serializers.CharField()
    alrt_orgi_orga_dk = serializers.IntegerField()
    alrt_docu_dk = serializers.IntegerField()
    alrt_docu_nr_mp = serializers.CharField()
    alrt_date_referencia = serializers.DateTimeField(format="%Y-%m-%d")
    alrt_dias_referencia = serializers.IntegerField()
    alrt_dk_referencia = serializers.IntegerField()
    alrt_info_adicional = serializers.CharField()


class AlertasROSerializer(serializers.Serializer):
    alrt_key = serializers.CharField()
    alrt_sigla = serializers.CharField()
    alrt_orgi_orga_dk = serializers.IntegerField()
    ro_nr_delegacia = serializers.IntegerField()
    ro_qt_ros_faltantes = serializers.IntegerField()
    ro_max_proc = serializers.CharField()
