from django.conf import settings
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.db_connectors import run_query
from dominio.mixins import CacheMixin, JWTAuthMixin
from dominio.suamesa import format_text


class RadarView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'RADAR_CACHE_TIMEOUT'
    field_names = [
        "cod_pct",
        "pacote_atribuicao",
        "orgao_id",
        "nr_arquivamentos",
        "nr_indeferimentos",
        "nr_instauracoes",
        "nr_tac",
        "nr_acoes",
        "max_pacote_arquivamentos",
        "max_pacote_indeferimentos",
        "max_pacote_instauracoes",
        "max_pacote_tac",
        "max_pacote_acoes",
        "perc_arquivamentos",
        "perc_indeferimentos",
        "perc_instauracoes",
        "perc_acoes",
        "perc_tac",
        "med_pacote_aquivamentos",
        "med_pacote_tac",
        "med_pacote_indeferimentos",
        "med_pacote_instauracoes",
        "med_pacote_acoes",
        "var_med_arquivamentos",
        "var_med_tac",
        "var_med_indeferimentos",
        "var_med_instauracoes",
        "var_med_acoes",
        "dt_calculo",
        "nm_max_arquivamentos",
        "nm_max_indeferimentos",
        "nm_max_instauracoes",
        "nm_max_tac",
        "nm_max_acoes",
    ]

    def prepare_response(self, resp):
        format_fields = [
            "nm_max_arquivamentos", "nm_max_indeferimentos",
            "nm_max_instauracoes", "nm_max_tac", "nm_max_acoes"
        ]
        for field in format_fields:
            resp[field] = format_text(resp[field])

        return resp

    def get_radar_data(self, orgao_id):
        query = """
            SELECT * FROM {schema}.tb_radar_performance
            WHERE orgao_id = :orgao_id
        """
        f_query = query.format(
                schema=settings.TABLE_NAMESPACE
        )
        parameters = {"orgao_id": orgao_id}

        return run_query(f_query, parameters=parameters)

    def parse_orgao_id(self, orgao_id):
        try:
            orgao_id = int(orgao_id)
        except ValueError:
            raise Http404("Valor <orgao_id> inválido")

        return orgao_id

    def get(self, request, *args, **kwargs):
        orgao_id = self.parse_orgao_id(kwargs.get("orgao_id"))

        radar_data = self.get_radar_data(orgao_id)
        if radar_data is None:
            raise Http404

        resp_data = self.prepare_response(
            dict(zip(self.field_names, radar_data[0]))
        )
        return Response(data=resp_data)
