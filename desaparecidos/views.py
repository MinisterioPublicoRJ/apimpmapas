from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from desaparecidos.dao import client, rank


class DesaparecidosView(APIView):
    def get(self, request, *args, **kwargs):
        cursor = client(
            settings.DESAPARECIDOS_DB_USER,
            settings.DESAPARECIDOS_DB_PWD,
            settings.DESAPARECIDOS_DB_HOST
        )
        result = rank(cursor, kwargs.get("id_sinalid"))
        status = 404 if "erro" in result else 200
        return Response(result, status=status)
