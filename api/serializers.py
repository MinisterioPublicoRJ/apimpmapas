from rest_framework import serializers

from api.models import Entidade


class EntidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidade
        fields = '__all__'
