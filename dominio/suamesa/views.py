from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.mixins import CacheMixin, JWTAuthMixin
from dominio.suamesa.dao import (
    DocumentoDAO,
    SuaMesaDAO,
    SuaMesaDetalheFactoryDAO
)


class DocumentosDetalheView(CacheMixin, APIView):
    cache_config = 'DOCUMENTO_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        num_mprj = int(kwargs.get("num_mprj"))

        data = DocumentoDAO.get(num_mprj, request)

        return Response(data=data)


class SuaMesaView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESA_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        data = SuaMesaDAO.get(orgao_id, request)

        return Response(data=data)


class SuaMesaDetalheView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESA_DETALHE_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        data = SuaMesaDetalheFactoryDAO.get(orgao_id, request)

        return Response(data=data)
