from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.mixins import JWTAuthMixin


class SecureView(JWTAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response(data={})
