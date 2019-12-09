from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from desaparecidos.tasks import async_calculate_rank


class DesaparecidosView(APIView):
    def post(self, request, *args, **kwargs):
        id_sinalid = kwargs.pop('id_sinalid')
        cache_resp = cache.get(id_sinalid)
        if cache_resp is None:
            async_calculate_rank(id_sinalid)
        return Response()
