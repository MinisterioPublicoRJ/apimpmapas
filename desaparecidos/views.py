from rest_framework.response import Response
from rest_framework.views import APIView

from desaparecidos.dao import rank


class DesaparecidosView(APIView):
    def get(self, request, *args, **kwargs):
        result = rank(kwargs.get("id_sinalid"))
        status = 404 if "erro" in result else 200
        return Response(result, status=status)
