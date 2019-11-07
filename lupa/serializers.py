import json

from rest_framework import serializers

from .db_connectors import execute
from .exceptions import QueryError
from .models import (
    Entidade,
    DadoEntidade,
    DadoDetalhe,
    TipoDado,
    ColunaDado,
    ColunaDetalhe,
    ColunaMapa,
)


def calculate_total(data_list):
    total = 0
    for data in data_list:
        if data['dado']:
            total += float(data['dado'])
    return total


def rowToExternalData(row, column_list):
    data = {}
    for i, item in enumerate(column_list):
        data[item['info_type']] = row[i]
    return data


def rowToMapData(row, column_list):
    feature = {}
    feature['type'] = 'Feature'
    feature['properties'] = {}

    for i, item in enumerate(column_list):
        if item['info_type'] == 'geojson':
            feature['geometry'] = json.loads(row[i])
        else:
            feature['properties'][item['info_type']] = row[i]
    return feature


class DadoEntidadeInternalSerializer(serializers.ModelSerializer):
    theme_name = serializers.SerializerMethodField()
    theme_color = serializers.SerializerMethodField()

    class Meta:
        model = DadoEntidade
        fields = ['id', 'theme_name', 'theme_color']

    def get_theme_name(self, obj):
        if obj.theme:
            return obj.theme.name
        return None

    def get_theme_color(self, obj):
        if obj.theme:
            return obj.theme.color
        return None


class DadoDetalheInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadoDetalhe
        fields = ['id']


class DataColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColunaDado
        fields = ['name', 'info_type']


class DetailColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColunaDetalhe
        fields = ['name', 'info_type']


class MapColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColunaMapa
        fields = ['name', 'info_type']


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
            column_list = MapColumnSerializer(
                obj.map_info.column_list.all(),
                many=True,
                read_only=True
            ).data

            columns = []
            id_column = None
            for column in column_list:
                columns.append('{} as {}'.format(
                    column['name'],
                    column['info_type']
                ))
                if column['info_type'] == 'id':
                    id_column = column['name']

            try:
                db_result = execute(
                    obj.map_info.database,
                    obj.map_info.schema,
                    obj.map_info.table,
                    columns,
                    id_column,
                    str(self.base_data['domain_id'])
                )
            except QueryError:
                return None

            if db_result:
                features = []
                for main_result in db_result:
                    feature = rowToMapData(main_result, column_list)
                    features.append(feature)
                return features
        return None

    def get_theme_list(self, obj):
        data_list = DadoEntidadeInternalSerializer(
            obj.obter_dados().filter(show_box=True),
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
        if theme:
            theme_list.append(theme)

        return theme_list


class DadoEntidadeSerializer(serializers.ModelSerializer):
    external_data = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    data_type = serializers.SerializerMethodField()
    detalhe = serializers.SerializerMethodField()

    class Meta:
        model = DadoEntidade
        fields = [
            'id',
            'exibition_field',
            'external_data',
            'data_type',
            'icon',
            'detalhe',
        ]

    def __init__(self, *args, **kwargs):
        self.domain_id = str(kwargs.pop('domain_id'))

        dado = args[0]
        self.data_type = dado.data_type.name
        super().__init__(*args, **kwargs)

    def get_external_data(self, obj):
        column_list = DataColumnSerializer(
            obj.column_list.all(),
            many=True,
            read_only=True
        ).data

        columns = []
        id_column = None
        for column in column_list:
            columns.append('{} as {}'.format(
                column['name'],
                column['info_type']
            ))
            if column['info_type'] == 'id':
                id_column = column['name']

        try:
            db_result = execute(
                obj.database,
                obj.schema,
                obj.table,
                columns,
                id_column,
                self.domain_id
            )
        except QueryError:
            return {}

        if db_result:
            if obj.data_type.serialization == TipoDado.SINGLETON_DATA:
                data = rowToExternalData(
                    row=db_result[0],
                    column_list=column_list
                )
                return data
            elif (obj.data_type.serialization == TipoDado.LIST_DATA or
                  obj.data_type.serialization == TipoDado.XY_GRAPH_DATA):
                data = []
                for result in db_result:
                    data.append(
                        rowToExternalData(row=result, column_list=column_list)
                    )
                if obj.limit_fetch > 0:
                    return data[:obj.limit_fetch]
                return data
            elif obj.data_type.serialization == TipoDado.PIZZA_GRAPH_DATA:
                data = []
                for result in db_result:
                    data.append(
                        rowToExternalData(row=result, column_list=column_list)
                    )

                total = calculate_total(data)

                outros = None
                data_rev = []
                for line in data:
                    if line['dado']/total <= 0.03:
                        if outros:
                            outros['dado'] += line['dado']
                        else:
                            outros = {
                                'dado': line['dado'],
                                'rotulo': 'Outros'
                            }
                    else:
                        data_rev.append(line)
                if outros:
                    data_rev.append(outros)
                return data_rev
        return {}

    def get_icon(self, obj):
        if obj.icon:
            icon_url = obj.icon.file_path.url
            return icon_url
        return None

    def get_data_type(self, obj):
        return obj.data_type.name

    def get_detalhe(self, obj):
        detail_list = DadoDetalheInternalSerializer(
            obj.data_details.all(),
            many=True,
            read_only=True
        ).data
        return detail_list


class DadoDetalheSerializer(serializers.ModelSerializer):
    external_data = serializers.SerializerMethodField()
    data_type = serializers.SerializerMethodField()

    class Meta:
        model = DadoEntidade
        fields = [
            'id',
            'exibition_field',
            'external_data',
            'data_type',
        ]

    def __init__(self, *args, **kwargs):
        self.domain_id = str(kwargs.pop('domain_id'))

        dado = args[0]
        self.data_type = dado.data_type.name
        super().__init__(*args, **kwargs)

    def get_external_data(self, obj):
        column_list = DetailColumnSerializer(
            obj.column_list.all(),
            many=True,
            read_only=True
        ).data

        columns = []
        id_column = None
        for column in column_list:
            columns.append('{} as {}'.format(
                column['name'],
                column['info_type']
            ))
            if column['info_type'] == 'id':
                id_column = column['name']

        try:
            db_result = execute(
                obj.database,
                obj.schema,
                obj.table,
                columns,
                id_column,
                self.domain_id
            )
        except QueryError:
            return {}

        if db_result:
            if obj.data_type.serialization == TipoDado.SINGLETON_DATA:
                data = rowToExternalData(
                    row=db_result[0],
                    column_list=column_list
                )
                return data
            elif (obj.data_type.serialization == TipoDado.LIST_DATA or
                  obj.data_type.serialization == TipoDado.XY_GRAPH_DATA):
                data = []
                for result in db_result:
                    data.append(
                        rowToExternalData(row=result, column_list=column_list)
                    )
                if obj.limit_fetch > 0:
                    return data[:obj.limit_fetch]
                return data
            elif obj.data_type.serialization == TipoDado.PIZZA_GRAPH_DATA:
                data = []
                for result in db_result:
                    data.append(
                        rowToExternalData(row=result, column_list=column_list)
                    )

                total = calculate_total(data)

                outros = None
                data_rev = []
                for line in data:
                    if line['dado']/total <= 0.03:
                        if outros:
                            outros['dado'] += line['dado']
                        else:
                            outros = {
                                'dado': line['dado'],
                                'rotulo': 'Outros'
                            }
                    else:
                        data_rev.append(line)
                if outros:
                    data_rev.append(outros)
                return data_rev
        return {}

    def get_data_type(self, obj):
        return obj.data_type.name


class EntidadeIdSerializer(serializers.ModelSerializer):
    entity_id = serializers.SerializerMethodField()

    class Meta:
        model = Entidade
        fields = [
            'abreviation',
            'entity_id'
        ]

    def __init__(self, *args, **kwargs):
        self._entity_id = kwargs.pop('entity_id')
        super().__init__(*args, **kwargs)

    def get_entity_id(self, obj):
        return str(self._entity_id)
