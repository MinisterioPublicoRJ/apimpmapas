import json

from rest_framework import serializers

from api.db_connectors import execute
from api.exceptions import QueryError
from api.models import TipoEntidade, Entidade, Dado


class EntidadeSerializer(serializers.ModelSerializer):
    data_list = serializers.SerializerMethodField()
    entity_type = serializers.SerializerMethodField()
    geojson = serializers.SerializerMethodField()

    class Meta:
        model = Entidade
        fields = [
            'id',
            'data_list',
            'domain_id',
            'exibition_field',
            'entity_type',
            'geojson',
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

    def get_geojson(self, obj):
        if (obj.map_table) and (obj.map_column_id) and (obj.map_column_geom):
            try:
                db_result = execute(
                    'PG',
                    'lupa',
                    obj.map_table,
                    [obj.map_column_geom, ],
                    obj.map_column_id,
                    obj.domain_id
                )
            except QueryError:
                return None

            if db_result:
                main_result = db_result[0]

                return json.loads(main_result[0])

        return None


class TipoEntidadeSerializer(serializers.ModelSerializer):
    domain_id = serializers.SerializerMethodField()
    entity_type = serializers.SerializerMethodField()
    exibition_field = serializers.SerializerMethodField()
    data_list = serializers.SerializerMethodField()
    geojson = serializers.SerializerMethodField()

    class Meta:
        model = TipoEntidade
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

    def get_entity_type(self, obj):
        return obj.name

    def get_exibition_field(self, obj):
        return self.base_data['exibition_field']

    def get_domain_id(self, obj):
        return self.base_data['domain_id']

    def get_geojson(self, obj):
        return self.base_data['geojson']

    def get_data_list(self, obj):
        return Dado.objects.filter(entity_type=obj.abreviation).values('id')


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
