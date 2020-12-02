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


class ListaProcessosSerializer(serializers.Serializer):
    id_orgao = serializers.IntegerField()
    classe_documento = serializers.CharField()
    docu_nr_mp = serializers.CharField()
    docu_nr_externo = serializers.CharField()
    docu_etiqueta = serializers.CharField()
    docu_personagens = serializers.CharField()
    representante_dk = serializers.IntegerField()
    dt_ultimo_andamento = serializers.DateTimeField(format="%Y-%m-%d")
    ultimo_andamento = serializers.CharField()
    url_tjrj = serializers.CharField()


class RadarPerformanceSerializer(serializers.Serializer):
    cod_pct = serializers.IntegerField()
    pacote_atribuicao = serializers.CharField()
    orgao_id = serializers.IntegerField()
    nr_arquivamentos = serializers.IntegerField(min_value=0)
    nr_indeferimentos = serializers.IntegerField(min_value=0)
    nr_instauracoes = serializers.IntegerField(min_value=0)
    nr_tac = serializers.IntegerField(min_value=0)
    nr_acoes = serializers.IntegerField(min_value=0)
    max_pacote_arquivamentos = serializers.IntegerField(min_value=0)
    max_pacote_indeferimentos = serializers.IntegerField(min_value=0)
    max_pacote_instauracoes = serializers.IntegerField(min_value=0)
    max_pacote_tac = serializers.IntegerField(min_value=0)
    max_pacote_acoes = serializers.IntegerField(min_value=0)
    perc_arquivamentos = serializers.FloatField()
    perc_indeferimentos = serializers.FloatField()
    perc_instauracoes = serializers.FloatField()
    perc_tac = serializers.FloatField()
    perc_acoes = serializers.FloatField()
    med_pacote_aquivamentos = serializers.FloatField()
    med_pacote_indeferimentos = serializers.FloatField()
    med_pacote_instauracoes = serializers.FloatField()
    med_pacote_tac = serializers.FloatField()
    med_pacote_acoes = serializers.FloatField()
    var_med_arquivamentos = serializers.FloatField()
    var_med_indeferimentos = serializers.FloatField()
    var_med_instauracoes = serializers.FloatField()
    var_med_tac = serializers.FloatField()
    var_med_acoes = serializers.FloatField()
    dt_calculo = serializers.DateTimeField()
    nm_max_arquivamentos = serializers.CharField()
    nm_max_indeferimentos = serializers.CharField()
    nm_max_instauracoes = serializers.CharField()
    nm_max_tac = serializers.CharField()
    nm_max_acoes = serializers.CharField()
