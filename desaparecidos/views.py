from rest_framework.response import Response
from rest_framework.views import APIView

from desaparecidos.tasks import async_calculate_rank


class DesaparecidosView(APIView):
    def post(self, request, *args, **kwargs):
        id_sinalid = kwargs.pop('id_sinalid')
        async_calculate_rank(id_sinalid)
        return Response()
