from rest_framework import serializers


class OutliersSerializer(serializers.Serializer):
    cod_orgao = serializers.IntegerField()
    acervo_qtd = serializers.IntegerField(min_value=0)
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
    dt_inclusao = serializers.DateTimeField()


class SaidasSerializer(serializers.Serializer):
    saidas = serializers.IntegerField(min_value=0)
    id_orgao = serializers.IntegerField()
    cod_pct = serializers.IntegerField()
    percent_rank = serializers.FloatField()
    dt_calculo = serializers.DateTimeField()


class EntradasSerializer(serializers.Serializer):
    nr_entradas_hoje = serializers.IntegerField(min_value=0)
    minimo = serializers.IntegerField(min_value=0)
    maximo = serializers.IntegerField(min_value=0)
    media = serializers.FloatField()
    primeiro_quartil = serializers.FloatField()
    mediana = serializers.FloatField()
    terceiro_quartil = serializers.FloatField()
    iqr = serializers.FloatField()
    lout = serializers.FloatField()
    hout = serializers.FloatField()


class SuaMesaSerializer(serializers.Serializer):
    vistas_abertas = serializers.IntegerField(min_value=0)
    investigacoes_curso = serializers.IntegerField(min_value=0)
    processos_juizo = serializers.IntegerField(min_value=0)
    finalizados = serializers.IntegerField(min_value=0)


class SuaMesaListaVistasSerializer(serializers.Serializer):
    numero_mprj = serializers.CharField()
    numero_externo = serializers.CharField()
    dt_abertura = serializers.DateField()
    classe = serializers.CharField()


class DetalheAcervoSerializer(serializers.Serializer):

    class VariacaoPromotoriaSerializer(serializers.Serializer):
        nm_promotoria = serializers.CharField()
        variacao_acervo = serializers.FloatField(min_value=0)

    variacao_acervo = serializers.FloatField()
    top_n = VariacaoPromotoriaSerializer(many=True)


class DetalheProcessosJuizoSerializer(serializers.Serializer):

    class AcoesPromotoriaSerializer(serializers.Serializer):
        nm_promotoria = serializers.CharField()
        nr_acoes_propostas_30_dias = serializers.IntegerField(min_value=0)

    nr_acoes_propostas_60_dias = serializers.IntegerField(min_value=0)
    variacao_12_meses = serializers.FloatField()
    top_n = AcoesPromotoriaSerializer(many=True)


class AlertasListaSerializer(serializers.Serializer):
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


# Ver como deixar isso mais bonito
class AproveitamentosPIPSerializer(serializers.Serializer):
    nm_promotoria = serializers.CharField()
    nr_aproveitamentos_30_dias = serializers.IntegerField(min_value=0)


class PIPDetalheAproveitamentosSerializer(serializers.Serializer):
    class TopNByAISPSerializer(serializers.Serializer):
        nr_aisp = serializers.IntegerField()
        top_n = AproveitamentosPIPSerializer(many=True)

    nr_aproveitamentos_30_dias = serializers.IntegerField(min_value=0)
    variacao_1_mes = serializers.FloatField()
    top_n_pacote = AproveitamentosPIPSerializer(many=True)
    top_n_by_aisp = TopNByAISPSerializer(many=True)
