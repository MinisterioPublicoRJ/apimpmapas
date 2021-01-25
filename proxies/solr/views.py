import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from login.simple import token_required
from proxies.login.permissions import SCARolePermission
from proxies.solr.client import SolrClient, create_solr_client
from proxies.solr.serializers import (
    SolrCadUnicoSerializer,
    SolrPlacasSerializer,
)
from pysolr import SolrError

from proxies.solr.exceptions import ServiceUnavailable


logger = logging.getLogger(__name__)


class SolrPlacasView(GenericAPIView):
    serializer_class = SolrPlacasSerializer
    permission_classes = (SCARolePermission,)
    permission_roles = (settings.PROXIES_PLACAS_ROLE,)

    def get_data(self, query, start, rows):
        try:
            data = create_solr_client().search(query, start, rows)
        except SolrError as e:
            logger.error(
                "query={query} - params:{start} | {rows}: {e!r}".format(
                    query=query,
                    start=start,
                    rows=rows,
                    e=e
                )
            )
            raise ServiceUnavailable

        return data

    def get(self, request, *args, **kwargs):
        ser = self.get_serializer_class()(data=request.GET)
        ser.is_valid(raise_exception=True)
        data = self.get_data(
            ser.validated_data["query"],
            ser.validated_data["start"],
            ser.validated_data["rows"],
        )
        logger.info(
            f"Consulta de 'placas' feita por {request.sca_username}"
        )
        return Response(data=data)


class SolrCadUnicoPessoaView(GenericAPIView):
    serializer_class = SolrCadUnicoSerializer

    def get_data(self, query, start, rows):
        try:
            data = SolrClient.request_query(query)
        except Exception as e:
            logger.error(
                "query={query} - params:{start} | {rows}: {e!r}".format(
                    query=query,
                    start=start,
                    rows=rows,
                    e=e
                )
            )
            raise ServiceUnavailable

        return data

    @token_required(token_conf_var="CADUNICO_AUTH_TOKEN")
    def get(self, request, *args, **kwargs):
        query = (
            'cadunico_pessoa/select?q=%22{f_q}%22&'
            'wt=json&indent=true&defType=edismax&qf=no_pessoa+'
            'no_completo_mae_pessoa+nu_cpf_pessoa&qs=1&stopwords=true&'
            'lowercaseOperators=true&hl=true%22&sort=score%20DESC'
        )
        ser = self.get_serializer_class()(data=request.GET)
        ser.is_valid(raise_exception=True)
        f_query = query.format(f_q=ser.validated_data["f_q"])
        data = self.get_data(
            f_query,
            start=1,
            rows=10,
        )
        logger.info(
            f"Consulta em 'cadunico-pessoa'"
        )
        return Response(data=data)
