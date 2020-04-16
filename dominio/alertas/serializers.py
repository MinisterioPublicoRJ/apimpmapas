from rest_framework import serializers


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
