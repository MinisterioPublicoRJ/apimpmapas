from rest_framework import serializers

from api.db_connectors import execute
from api.exceptions import QueryError
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
    external_data = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Dado
        fields = [
            'id',
            'external_data',
            'exibition_field',
            'data_type',
            'icon'
        ]

    def __init__(self, *args, **kwargs):
        self.domain_id = kwargs.pop('domain_id')
        super().__init__(*args, **kwargs)

    def get_external_data(self, obj):
        columns = []
        columns.append(obj.data_column)
        columns.append(
            obj.source_column if obj.source_column else 'NULL as fonte'
        )
        columns.append(
            obj.details_column if obj.details_column else 'NULL as detalhes'
        )
        try:
            db_result = execute(
                obj.database,
                obj.schema,
                obj.table,
                columns,
                obj.id_column,
                self.domain_id
            )
        except QueryError:
            return {}

        if db_result:
            main_result = db_result[0]

            data = {
                'dado': main_result[0],
                'fonte': main_result[1],
                'descricao': main_result[2],
            }

            return data

        return {}

    def get_data_type(self, obj):
        if obj.data_type == 'TEX_GDE':
            return 'texto_grande'
        elif obj.data_type == 'TEX_PEQ':
            return 'texto_pequeno'
        elif obj.data_type == 'TEX_PEQ_DEST':
            return 'texto_pequeno_destaque'

        return 'tipo_desconhecido'

    def get_icon(self, obj):
        if obj.icon:
            icon_url = obj.icon.file_path.url
            return icon_url
        return None
