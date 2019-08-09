import json

from rest_framework import serializers

from api.db_connectors import execute
from api.exceptions import QueryError
from api.models import (
    Entidade,
    Dado,
    SINGLETON_DATA,
    LIST_DATA,
    GRAPH_DATA
)


class DadoInternalSerializer(serializers.ModelSerializer):
    theme_name = serializers.SerializerMethodField()
    theme_color = serializers.SerializerMethodField()

    class Meta:
        model = Dado
        fields = ['id', 'theme_name', 'theme_color']

    def get_theme_name(self, obj):
        if obj.theme:
            return obj.theme.name
        return None

    def get_theme_color(self, obj):
        if obj.theme:
            return obj.theme.color
        return None


class EntidadeSerializer(serializers.ModelSerializer):
    entity_type = serializers.CharField(source='name')
    domain_id = serializers.SerializerMethodField()
    exibition_field = serializers.SerializerMethodField()
    geojson = serializers.SerializerMethodField()
    theme_list = serializers.SerializerMethodField()

    class Meta:
        model = Entidade
        fields = [
            'domain_id',
            'entity_type',
            'exibition_field',
            'geojson',
            'theme_list',
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
            'exibition_field': None
        }

        db_result = None
        try:
            db_result = execute(
                tipo_entidade.database,
                tipo_entidade.schema,
                tipo_entidade.table,
                [tipo_entidade.name_column],
                tipo_entidade.id_column,
                domain_id
            )
        except QueryError:
            pass
        if db_result:
            main_result = db_result[0]
            data['exibition_field'] = main_result[0]

        return data

    def get_exibition_field(self, obj):
        return self.base_data['exibition_field']

    def get_domain_id(self, obj):
        return self.base_data['domain_id']

    def get_geojson(self, obj):
        if hasattr(obj, 'map_info') and obj.map_info:
            db_result = None
            try:
                columns = [
                    obj.map_info.geom_column,
                    obj.map_info.label_column,
                    obj.map_info.related_entity_column,
                    obj.map_info.related_id_column
                ]
                db_result = execute(
                    obj.map_info.database,
                    obj.map_info.schema,
                    obj.map_info.table,
                    columns,
                    obj.map_info.entity_id_column,
                    self.base_data['domain_id']
                )
            except QueryError:
                return None
            if db_result:
                features = []
                for main_result in db_result:
                    feature = {}
                    feature['geometry'] = json.loads(main_result[0])
                    feature['type'] = 'Feature'
                    feature['properties'] = {}
                    feature['properties']['name'] = main_result[1]
                    feature['properties']['entity_link_type'] = main_result[2]
                    feature['properties']['entity_link_id'] = main_result[3]
                    features.append(feature)
                return features
        return None

    def get_theme_list(self, obj):
        data_list = DadoInternalSerializer(
            obj.data_list.all(),
            many=True,
            read_only=True
        ).data

        theme_list = []
        theme = None

        for data in data_list:
            if not theme or theme['tema'] != data['theme_name']:
                if theme:
                    theme_list.append(theme)
                theme = {
                    'tema': data['theme_name'],
                    'cor': data['theme_color'],
                    'data_list': []
                }
            data_id = {}
            data_id['id'] = data['id']
            theme['data_list'].append(data_id)
        theme_list.append(theme)

        return theme_list


class DadoSerializer(serializers.ModelSerializer):
    external_data = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    data_type = serializers.SerializerMethodField()

    class Meta:
        model = Dado
        fields = [
            'id',
            'exibition_field',
            'external_data',
            'data_type',
            'icon'
        ]

    def __init__(self, *args, **kwargs):
        self.domain_id = str(kwargs.pop('domain_id'))

        dado = args[0]
        self.data_type = dado.data_type.name
        super().__init__(*args, **kwargs)

    def get_external_data(self, obj):
        columns = []
        columns.append(obj.data_column)
        columns.append(
            obj.label_column if obj.label_column else 'NULL as rotulo'
        )
        columns.append(
            obj.source_column if obj.source_column else 'NULL as fonte'
        )
        columns.append(
            obj.details_column if obj.details_column else 'NULL as detalhes'
        )
        columns.append(
            obj.entity_link_id_column
            if obj.entity_link_id_column
            else 'NULL as link_interno_id'
        )
        columns.append(
            obj.external_link_column
            if obj.external_link_column
            else 'NULL as link_externo'
        )
        columns.append(
            obj.image_column if obj.image_column else 'NULL as imagem'
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
            if obj.data_type.serialization == SINGLETON_DATA:
                result = db_result[0]
                data = {
                    'dado': result[0],
                    'rotulo': result[1],
                    'fonte': result[2],
                    'detalhes': result[3],
                    'imagem': result[6],
                    'link_interno_entidade':
                        obj.entity_link_type.abreviation
                        if obj.entity_link_type
                        else None,
                    'link_interno_id': result[4],
                    'link_externo': result[5]
                }
                return data
            elif (obj.data_type.serialization == LIST_DATA or
                  obj.data_type.serialization == GRAPH_DATA):
                data = []
                for result in db_result:
                    data_dict = {
                        'dado': result[0],
                        'rotulo': result[1],
                        'fonte': result[2],
                        'detalhes': result[3],
                        'imagem': result[6],
                        'link_interno_entidade':
                            obj.entity_link_type.abreviation
                            if obj.entity_link_type
                            else None,
                        'link_interno_id': result[4],
                        'link_externo': result[5]
                    }
                    data.append(data_dict)
                if obj.limit_fetch > 0:
                    return data[:obj.limit_fetch]
                return data
        return {}

    def get_icon(self, obj):
        if obj.icon:
            icon_url = obj.icon.file_path.url
            return icon_url
        return None

    def get_data_type(self, obj):
        return obj.data_type.name
