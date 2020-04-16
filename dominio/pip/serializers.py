from rest_framework import serializers


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
