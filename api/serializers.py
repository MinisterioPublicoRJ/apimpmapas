import json

from rest_framework import serializers

from api.db_connectors import execute
from api.exceptions import QueryError
from api.models import (
    Entidade,
    Dado,
    TEXT_GDE,
    TEXT_PEQ,
    TEXT_PEQ_DEST,
    LIST_UNRANK,
    LIST_RANKED,
    # GRAPH_BAR_VERT,
    # GRAPH_BAR_HORI,
    # GRAPH_PIZZA
)


class DadoInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dado
        fields = ['id', ]


class EntidadeSerializer(serializers.ModelSerializer):
    entity_type = serializers.CharField(source='name')
    domain_id = serializers.SerializerMethodField()
    exibition_field = serializers.SerializerMethodField()
    geojson = serializers.SerializerMethodField()
    data_list = serializers.SerializerMethodField()

    class Meta:
        model = Entidade
        fields = [
            'domain_id',
            'entity_type',
            'exibition_field',
            'geojson',
            'data_list',
        ]

    def __init__(self, *args, **kwargs):
        tipo_entidade = args[0]
        self.base_data = self.get_base_data(
            tipo_entidade,
            kwargs.pop('domain_id')
        )
        super().__init__(*args, **kwargs)

    def get_base_data(self, tipo_entidade, domain_id):
        data = {
            'domain_id': domain_id,
            'exibition_field': None,
            'geojson': None
        }

        columns = [tipo_entidade.name_column]
        if tipo_entidade.geom_column:
            columns.append(tipo_entidade.geom_column)

        try:
            db_result = execute(
                tipo_entidade.database,
                tipo_entidade.schema,
                tipo_entidade.table,
                columns,
                tipo_entidade.id_column,
                domain_id
            )
        except QueryError:
            return data

        if db_result:
            main_result = db_result[0]
            data['exibition_field'] = main_result[0]
            if tipo_entidade.geom_column:
                data['geojson'] = json.loads(main_result[1])

        return data

    def get_exibition_field(self, obj):
        return self.base_data['exibition_field']

    def get_domain_id(self, obj):
        return self.base_data['domain_id']

    def get_geojson(self, obj):
        return self.base_data['geojson']

    def get_data_list(self, obj):
        data_list = obj.data_list.all()
        return DadoInternalSerializer(
            data_list,
            many=True,
            read_only=True).data


class DadoSerializer(serializers.ModelSerializer):
    external_data = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    exibition_field = serializers.SerializerMethodField()

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
            obj.label_column if obj.label_column else 'NULL as label'
        )
        columns.append(
            obj.source_column if obj.source_column else 'NULL as fonte'
        )
        columns.append(
            obj.details_column if obj.details_column else 'NULL as detalhes'
        )
        columns.append(
            obj.link_column if obj.link_column else 'NULL as link'
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
            if obj.data_type in [TEXT_GDE, TEXT_PEQ, TEXT_PEQ_DEST]:
                result = db_result[0]
                data = {
                    'dado': result[0],
                    'label': result[1],
                    'fonte': result[2],
                    'detalhes': result[3],
                    'link': result[4],
                }
                return data
            elif obj.data_type in [LIST_UNRANK, LIST_RANKED]:
                data = []
                for result in db_result:
                    data_dict = {
                        'dado': result[0],
                        'label': result[1],
                        'fonte': result[2],
                        'detalhes': result[3],
                        'link': result[4],
                    }
                    data.append(data_dict)
                return data
        return {}

    def get_icon(self, obj):
        if obj.icon:
            icon_url = obj.icon.file_path.url
            return icon_url
        return None

    def get_exibition_field(self, obj):
        if obj.exibition_field:
            return obj.exibition_field
        return obj.title
