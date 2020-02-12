from busca_desaparecidos.dao import client, rank
from decouple import config
from rest_framework.response import Response
from rest_framework.views import APIView


class DesaparecidosView(APIView):
    def get(self, request, *args, **kwargs):
        cursor = client(
            config("DESAPARECIDOS_DB_USER"),
            config("DESAPARECIDOS_DB_PWD"),
            config("DESAPARECIDOS_DB_HOST")
        )
        return Response(rank(cursor, kwargs.get("id_sinalid")), status=200)
