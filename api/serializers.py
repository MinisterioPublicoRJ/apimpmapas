from rest_framework import serializers

from api.models import Entidade, Dado


class EntidadeSerializer(serializers.ModelSerializer):
    data_list = serializers.SerializerMethodField()

    class Meta:
        model = Entidade
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.entity_type = kwargs.pop('entity_type')
        super().__init__(*args, **kwargs)

    def get_data_list(self, obj):
        return Dado.objects.filter(entity_type=self.entity_type).values('id')
