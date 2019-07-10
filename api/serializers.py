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
        return 'Tipo_desconhecido'


class DadoSerializer(serializers.ModelSerializer):
    data_type = serializers.SerializerMethodField()
    external_data = serializers.SerializerMethodField(
        method_name="execute_query"
    )

    class Meta:
        model = Dado
        fields = [
            'id',
            'external_data',
            'exibition_field',
            'data_type'
        ]

    def __init__(self, *args, **kwargs):
        self.domain_id = kwargs.pop('domain_id')
        super().__init__(*args, **kwargs)

    def execute_query(self, obj):
        columns = []
        columns.append(obj.data_column)
        columns.append(obj.source_column if obj.source_column else 'NULL as fonte')
        columns.append(obj.details_column if obj.details_column else 'NULL as detalhes')

        db_result = execute(
            obj.database,
            obj.schema,
            obj.table,
            columns,
            obj.id_column,
            self.domain_id
        )
        data = {
            'dado': db_result[0],
            'fonte': db_result[1],
            'descricao': db_result[2],
        }

        return data

    def get_data_type(self, obj):
        if obj.data_type == 'TEX_GDE':
            return 'texto_grande'
        elif obj.data_type == 'TEX_PEQ':
            return 'texto_pequeno'
        elif obj.data_type == 'TEX_PEQ_DEST':
            return 'texto_pequeno_destaque'

        return 'tipo_desconhecido'
