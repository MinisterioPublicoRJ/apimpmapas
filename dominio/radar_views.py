from django.conf import settings
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.db_connectors import run_query
from dominio.radar_queries import field_names, query


@method_decorator(
    cache_page(
        settings.CACHE_TIMEOUT,
        key_prefix="dominio_radar"),
    name="dispatch"
)
class SuaPromotoriaView(APIView):
    def get_radar_data(self, orgao_id):
        f_query = query.format(
                orgao_id=orgao_id,
                schema=settings.TABLE_NAMESPACE
            )

        return run_query(f_query)

    def get(self, request, *args, **kwargs):
        orgao_id = kwargs.get("orgao_id")
        radar_data = self.get_radar_data(orgao_id)
        if radar_data is None:
            raise Http404

        return Response(data=dict(zip(field_names, radar_data[0])))
