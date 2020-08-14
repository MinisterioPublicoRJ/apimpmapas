from rest_framework import serializers


class ListaOrgaosSerializer(serializers.Serializer):
    cdorgao = serializers.CharField()
    nm_org = serializers.CharField()
    matricula = serializers.CharField()
    cpf = serializers.CharField()
    nome = serializers.CharField()
    sexo = serializers.CharField()
    pess_dk = serializers.CharField()


class PIPValidasSerializer(serializers.Serializer):
    id_orgao = serializers.CharField()


class DadosUsuarioSerializer(serializers.Serializer):
    matricula = serializers.CharField()
    cpf = serializers.CharField()
    nome = serializers.CharField()
    sexo = serializers.CharField()
    pess_dk = serializers.CharField()


class DPsPIPSerializer(serializers.Serializer):
    id_orgao = serializers.CharField()
    dps = serializers.CharField()
