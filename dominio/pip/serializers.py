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


class PIPPrincipaisInvestigadosPerfilSerializer(serializers.Serializer):
    pess_dk = serializers.IntegerField()
    nm_investigado = serializers.CharField()
    nm_mae = serializers.CharField()
    cpf = serializers.CharField()
    rg = serializers.CharField()
    dt_nasc = serializers.DateTimeField()
    nm_pesj = serializers.CharField()
    cnpj = serializers.CharField()


class PIPPrincipaisInvestigadosListaSerializer(serializers.Serializer):
    representante_dk = serializers.IntegerField()
    pess_dk = serializers.IntegerField()
    coautores = serializers.CharField()
    tipo_personagem = serializers.CharField()
    orgao_id = serializers.IntegerField()
    documento_nr_mp = serializers.CharField()
    documento_dt_cadastro = serializers.DateTimeField()
    documento_classe = serializers.CharField()
    nm_orgao = serializers.CharField()
    etiqueta = serializers.CharField()
    assuntos = serializers.ListField(serializers.CharField())
    fase_documento = serializers.CharField()
    dt_ultimo_andamento = serializers.DateTimeField()
    desc_ultimo_andamento = serializers.CharField()
    status_personagem = serializers.CharField()
    pers_dk = serializers.CharField()


class PIPIndicadoresSucessoParser(serializers.Serializer):
    orgao_id = serializers.IntegerField()
    indice = serializers.FloatField()
    tipo = serializers.CharField()
