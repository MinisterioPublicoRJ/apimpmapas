from datetime import date

from rest_framework import serializers

from dominio.documentos.helpers import formata_diff_data


class ComunicacaoCSMPSerializer(serializers.Serializer):
    nome_promotoria = serializers.CharField()
    num_procedimento = serializers.CharField()
    data_cadastro = serializers.SerializerMethodField()
    comarca = serializers.CharField()
    tempo_em_curso = serializers.SerializerMethodField()
    ementa = serializers.SerializerMethodField()
    investigados = serializers.CharField()

    def get_data_cadastro(self, obj):
        return obj["data_cadastro"].strftime("%d/%m/%Y")

    def get_tempo_em_curso(self, obj):
        return formata_diff_data(date.today(), obj["data_cadastro"])

    def get_ementa(self, obj):
        ementa = obj["ementa"]
        idx = ementa.find(";")
        if idx == 0:
            ementa = ementa[1:]

        return ementa
