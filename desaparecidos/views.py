from busca_desaparecidos.dao import client, rank
from rest_framework.response import Response
from rest_framework.views import APIView

from desaparecidos import settings as d_settings


class DesaparecidosView(APIView):
    def get(self, request, *args, **kwargs):
        cursor = client(
            d_settings.DESAPARECIDOS_DB_USER,
            d_settings.DESAPARECIDOS_DB_PWD,
            d_settings.DESAPARECIDOS_DB_HOST
        )
        result = rank(cursor, kwargs.get("id_sinalid"))
        status = 404 if "erro" in result.keys() else 200
        return Response(result, status=status)
