import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from proxies.login.permissions import SCARolePermission
from proxies.solr.client import create_solr_client
from proxies.solr.serializers import SolrPlacasSerializer
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
