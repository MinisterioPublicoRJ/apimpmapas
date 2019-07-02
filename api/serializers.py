from rest_framework import serializers

from api.db_connectors import execute
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


class DadoSerializer(serializers.ModelSerializer):
    external_data = serializers.SerializerMethodField(
        method_name="execute_query"
    )

    class Meta:
        model = Dado
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.domain_id = kwargs.pop('domain_id')
        super().__init__(*args, **kwargs)

    def execute_query(self, obj):
        return execute(obj.database, obj.query, self.domain_id)