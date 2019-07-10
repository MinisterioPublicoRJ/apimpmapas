from rest_framework import serializers

from api.db_connectors import execute
from api.models import Entidade, Dado


class EntidadeSerializer(serializers.ModelSerializer):
    data_list = serializers.SerializerMethodField()
    entity_type = serializers.SerializerMethodField()

    class Meta:
        model = Entidade
        fields = [
            'id',
            'data_list',
            'domain_id',
            'exibition_field',
            'entity_type',
        ]

    def __init__(self, *args, **kwargs):
        self.entity_type = kwargs.pop('entity_type')
        super().__init__(*args, **kwargs)

    def get_data_list(self, obj):
        return Dado.objects.filter(entity_type=self.entity_type).values('id')

    def get_entity_type(self, obj):
        if obj.entity_type == 'EST':
            return 'Estado'
        elif obj.entity_type == 'MUN':
            return 'Municipio'
        elif obj.entity_type == 'ORG':
            return 'Orgao'
        return 'Unknown'


class DadoSerializer(serializers.ModelSerializer):
    external_data = serializers.SerializerMethodField(
        method_name="execute_query"
    )

    class Meta:
        model = Dado
        exclude = [
            'title',
            'entity_type',
            'schema',
            'database',
            'table',
            'columns',
            'id_column'
        ]

    def __init__(self, *args, **kwargs):
        self.domain_id = kwargs.pop('domain_id')
        super().__init__(*args, **kwargs)

    def execute_query(self, obj):
        return execute(
            obj.database,
            obj.schema,
            obj.table,
            obj.columns,
            obj.id_column,
            self.domain_id
        )
