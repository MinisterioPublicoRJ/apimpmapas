from rest_framework import serializers


class ListaOrgaosSerializer(serializers.Serializer):
    cdorgao = serializers.CharField()
    nm_org = serializers.CharField()
    matricula = serializers.CharField()
    cpf = serializers.CharField()
    nome = serializers.CharField()
    sexo = serializers.CharField()
    pess_dk = serializers.CharField()


class DadosUsuarioSerializer(serializers.Serializer):
    matricula = serializers.CharField()
    cpf = serializers.CharField()
    nome = serializers.CharField()
    sexo = serializers.CharField()
    pess_dk = serializers.CharField()
