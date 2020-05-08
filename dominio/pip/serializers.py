from rest_framework import serializers


class PIPDetalheAproveitamentosSerializer(serializers.Serializer):
    class AproveitamentosPIPSerializer(serializers.Serializer):
        nm_promotoria = serializers.CharField()
        nr_aproveitamentos_periodo = serializers.IntegerField(min_value=0)

    nr_aproveitamentos_periodo = serializers.IntegerField(min_value=0)
    variacao_periodo = serializers.FloatField()
    top_n_pacote = AproveitamentosPIPSerializer(many=True)
    nr_aisps = serializers.ListField(serializers.IntegerField(min_value=0))
    top_n_aisp = AproveitamentosPIPSerializer(many=True)
    tamanho_periodo_dias = serializers.IntegerField(min_value=0)


class PIPPrincipaisInvestigadosSerializer(serializers.Serializer):
    nm_investigado = serializers.CharField()
    representante_dk = serializers.IntegerField()
    pip_codigo = serializers.IntegerField()
    nr_investigacoes = serializers.IntegerField(min_value=0)
    flag_multipromotoria = serializers.BooleanField()
    flag_top50 = serializers.BooleanField()


class PIPPrincipaisInvestigadosListaSerializer(serializers.Serializer):
    representante_dk = serializers.IntegerField()
    pip_codigo = serializers.IntegerField()
    docu_nr_mp = serializers.CharField()
    docu_dt_cadastro = serializers.DateTimeField()
    cldc_ds_classe = serializers.CharField()
    orgi_nm_orgao = serializers.CharField()
