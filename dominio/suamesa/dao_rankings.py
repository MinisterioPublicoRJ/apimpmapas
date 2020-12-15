from itertools import product

from django.conf import settings

from dominio.suamesa.serializers import (
    RankingSerializer,
    RankingFloatSerializer,
    RankingPercentageSerializer,
)
from dominio.dao import GenericDAO
from dominio.db_connectors import execute as impala_execute
from dominio.utils import format_text
from dominio.exceptions import APIEmptyResultError


class RankingDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "suamesa", "queries")
    query_file = "ranking_documento_orgao.sql"
    columns = [
        'nm_orgao',
        'valor',
    ]
    serializer = RankingSerializer
    table_namespaces = {
        "schema": settings.TABLE_NAMESPACE,
        "nm_campo": "{nm_campo}",
    }

    def __init__(self, ranking_fieldname):
        self.ranking_fieldname = ranking_fieldname

    def execute(self, **kwargs):
        return impala_execute(
            super().query().format(nm_campo=self.ranking_fieldname),
            kwargs
        )

    def serialize(self, result_set):
        result = super().serialize(result_set)
        for x in result:
            x['nm_orgao'] = format_text(x['nm_orgao'])
        return result

    def get(self, accept_empty=False, **kwargs):
        result_set = self.execute(**kwargs)
        if not result_set and not accept_empty:
            super().raise_empty_result_error()

        return self.serialize(result_set)


class RankingFloatDAO(RankingDAO):
    serializer = RankingFloatSerializer


class RankingPercentageDAO(RankingDAO):
    columns = [
        'nm_orgao',
        'valor_percentual',
    ]
    serializer = RankingPercentageSerializer


class RankingMixin:
    ranking_fields = []
    ranking_dao = RankingDAO

    @classmethod
    def get_ranking_data(cls, accept_empty=True, **kwargs):
        data = []

        # ranking_dao pode ser uma lista, um dao para cada ranking_field
        # Caso tenha mais fields do que DAOs, o zip irá excluir um desses
        # fields. O componente no front atualmente só pega os 2 primeiros
        if not isinstance(cls.ranking_dao, list):
            ranking_list = product(cls.ranking_fields, [cls.ranking_dao])
        else:
            ranking_list = zip(cls.ranking_fields, cls.ranking_dao)

        for fieldname, ranking_dao in ranking_list:
            dao = ranking_dao(fieldname)
            response = dao.get(accept_empty=accept_empty, **kwargs)
            if response:
                data.append({'ranking_fieldname': fieldname, 'data': response})

        return data

    @classmethod
    def get(cls, **kwargs):
        data = super().get(
            accept_empty=True,
            **kwargs
        )
        ranking_data = cls.get_ranking_data(**kwargs)

        # Intuito do Mixin simplesmente adicionar novos dados, verificação
        # do que existe ficaria mais pra frente. Mas pra ganhar tempo,
        # ficará assim por enquanto.
        if not data['metrics'] and not ranking_data:
            raise APIEmptyResultError

        data['rankings'] = ranking_data
        data['mapData'] = {}

        return data


class RankingFloatMixin(RankingMixin):
    ranking_dao = RankingFloatDAO


class RankingPercentageMixin(RankingMixin):
    ranking_dao = RankingPercentageDAO
