from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.mixins import CacheMixin, JWTAuthAllMixin
from dominio.pdfs.dao import ItGateDAO


class ItGateView(CacheMixin, APIView):
    cache_config = 'GATE_IT_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        it_gate_id = int(kwargs.get("it_gate_id"))

        data = ItGateDAO.get(it_gate_id, request)
        if 'erro' in data:
            return Response(data=data, status=404)
        else:
            response = HttpResponse(data, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="report.pdf"'
            return response
