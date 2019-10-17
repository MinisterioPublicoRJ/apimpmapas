import jwt

from decouple import config
from django.core.cache import cache as django_cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from jwt.exceptions import InvalidSignatureError, DecodeError
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    ListAPIView
)
from rest_framework.response import Response

from lupa.cache import cache_key
from .models import Entidade, Dado
from .serializers import (
    EntidadeSerializer,
    DadoSerializer,
    EntidadeIdSerializer
)
from .osmapi import query as osmquery
from .db_connectors import execute_geospatial


class EntityDataView:
    def process_request(self, request, obj, serializer, key_check):
        roles = obj.roles_allowed.all().values_list('role', flat=True)
        if roles:
            token = request.GET.get('auth_token')
            try:
                payload = jwt.decode(
                    token,
                    config('SECRET_KEY'),
                    algorithms=["HS256"]
                )
            except (InvalidSignatureError, DecodeError):
                return Response({}, status=403)
            permissions = payload['permissions']
            allowed = [role for role in roles if role in permissions]
            if not allowed:
                return Response({}, status=403)

        data = serializer(obj, domain_id=self.kwargs['domain_id']).data
        if not data[key_check]:
            raise Http404
        return Response(data)


class EntidadeView(GenericAPIView, EntityDataView):
    serializer_class = EntidadeSerializer
    queryset = Entidade.objects.all()

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            abreviation=self.kwargs['entity_type']
        )

        key = cache_key(key_prefix='lupa_entidade', kwargs=self.kwargs)
        if key in django_cache:
            response_data = django_cache.get(key)
            return Response(response_data)

        response = self.process_request(
            request,
            obj,
            EntidadeSerializer,
            'exibition_field'

        )
        django_cache.set(key, response.data)

        return self.process_request(
            request,
            obj,
            EntidadeSerializer,
            'exibition_field'
        )


class DadoView(RetrieveAPIView, EntityDataView):
    serializer_class = DadoSerializer
    queryset = Dado.objects.all()

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            entity_type__abreviation=self.kwargs['entity_type'],
            pk=self.kwargs['pk']
        )

        return self.process_request(
            request,
            obj,
            DadoSerializer,
            'external_data'
        )


@method_decorator(cache_page(600, key_prefix='lupa_osm'), name='dispatch')
class OsmQueryView(ListAPIView):
    queryset = []

    def get(self, request, *args, **kwargs):
        return Response(osmquery(self.kwargs['terms']))


@method_decorator(cache_page(600, key_prefix='lupa_geospat'), name='dispatch')
class GeoSpatialQueryView(ListAPIView):
    serializer_class = EntidadeIdSerializer
    queryset = []

    def get(self, request, lat, lon, value):
        entity_type = Entidade.objects.filter(
            osm_value_attached=value).first()

        if not entity_type:
            entity_type = Entidade.objects.filter(
                osm_default_level=True).first()

        if not entity_type:
            raise Http404

        entity = execute_geospatial(
            entity_type.database,
            entity_type.schema,
            entity_type.table,
            entity_type.geojson_column,
            entity_type.id_column,
            [lat, lon]
        )

        if not entity:
            raise Http404

        entity = entity[0][0]

        serializer = EntidadeIdSerializer(
                entity_type,
                entity_id=entity
            )
        return Response(serializer.data)
