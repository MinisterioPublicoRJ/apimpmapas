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
