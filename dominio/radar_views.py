from django.conf import settings
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.db_connectors import run_query
from dominio.radar_queries import field_names, query
from dominio.suamesa import format_text


@method_decorator(
    cache_page(
        settings.CACHE_TIMEOUT,
        key_prefix="dominio_radar"),
    name="dispatch"
)
class SuaPromotoriaView(APIView):
    def prepare_response(self, resp):
        resp["nm_max_arquivamentos"] = format_text(
            resp["nm_max_arquivamentos"]
        )
        resp["nm_max_indeferimentos"] = format_text(
            resp["nm_max_indeferimentos"]
        )
        resp["nm_max_instauracoes"] = format_text(
            resp["nm_max_instauracoes"]
        )
        resp["nm_max_tac"] = format_text(
            resp["nm_max_tac"]
        )
        resp["nm_max_acoes"] = format_text(
            resp["nm_max_acoes"]
        )

        return resp

    def get_radar_data(self, orgao_id):
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
            dict(zip(field_names, radar_data[0]))
        )
        return Response(data=resp_data)
