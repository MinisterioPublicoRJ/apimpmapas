from rest_framework import serializers


class ListaOrgaosSerializer(serializers.Serializer):
    cdorgao = serializers.CharField()
    matricula = serializers.CharField()
    cpf = serializers.CharField()
    nome = serializers.CharField()
    sexo = serializers.CharField()
    pess_dk = serializers.CharField()
    nm_org = serializers.CharField()
    grupo = serializers.CharField()
    atrib = serializers.CharField()


class ListaOrgaosPessoalSerializer(serializers.Serializer):
    cdorgao = serializers.CharField()
    nm_org = serializers.CharField()
    grupo = serializers.CharField()
    atrib = serializers.CharField()
