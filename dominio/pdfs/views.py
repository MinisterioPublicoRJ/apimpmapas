from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.mixins import CacheMixin, JWTAuthMixin
from dominio.pdfs.dao import ItGateDAO


class ItGateView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'GATE_IT_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        it_gate_id = int(kwargs.get("it_gate_id"))

        data = ItGateDAO.get(it_gate_id, request)
        status = 404 if "erro" in data else 200
        return Response(data=data, status=status)
