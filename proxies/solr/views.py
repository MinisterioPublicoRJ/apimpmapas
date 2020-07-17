from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from proxies.solr.client import create_solr_client
from proxies.solr.serializers import SolrPlacasSerializer


class SolrPlacasView(GenericAPIView):
    serializer_class = SolrPlacasSerializer

    def get_data(self, query, start, rows):
        return create_solr_client().search(query, start, rows)

    def get(self, request, *args, **kwargs):
        ser = self.get_serializer_class()(data=request.GET)
        if ser.is_valid(raise_exception=True):
            data = self.get_data(
                ser.validated_data["query"],
                ser.validated_data["start"],
                ser.validated_data["rows"],
            )
            return Response(data=data)
