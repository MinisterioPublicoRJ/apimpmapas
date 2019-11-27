import jwt

from decouple import config
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

from lupa.cache import (
    get_cache,
    save_cache,
    ENTITY_KEY_PREFIX,
    ENTITY_KEY_CHECK,
    DATA_ENTITY_KEY_PREFIX,
    DATA_ENTITY_KEY_CHECK,
    DATA_DETAIL_KEY_PREFIX,
    DATA_DETAIL_KEY_CHECK
)
from .models import Entidade, DadoDetalhe, DadoEntidade
from .serializers import (
    EntidadeSerializer,
    DadoDetalheSerializer,
    DadoEntidadeSerializer,
    EntidadeIdSerializer
)
from .osmapi import query as osmquery
from .db_connectors import execute_geospatial


def get_permissions(request):
    token = request.GET.get('auth_token')
    try:
        payload = jwt.decode(
            token,
            config('SECRET_KEY'),
            algorithms=["HS256"]
        )
    except (InvalidSignatureError, DecodeError):
        return []
    return payload['permissions']


class EntidadeView(GenericAPIView):
    serializer_class = EntidadeSerializer

    def get(self, request, *args, **kwargs):
        permissions = get_permissions(request)

        obj = get_object_or_404(
            Entidade.objects.get_authorized(permissions),
            abreviation=self.kwargs['entity_type']
        )

        # O cache é visto somente aqui, para garantir que
        # não bypasse as permissões
        cache = get_cache(ENTITY_KEY_PREFIX, kwargs)
        if cache:
            return cache

        data = EntidadeSerializer(obj, domain_id=self.kwargs['domain_id']).data
        if not data['exibition_field']:
            raise Http404

        if obj.is_cacheable:
            save_cache(data, ENTITY_KEY_PREFIX, ENTITY_KEY_CHECK, kwargs)

        return Response(data)


class DadoEntidadeView(RetrieveAPIView):
    serializer_class = DadoEntidadeSerializer

    def get(self, request, *args, **kwargs):
        permissions = get_permissions(request)

        obj = get_object_or_404(
            DadoEntidade.objects.get_authorized(permissions),
            entity_type__abreviation=self.kwargs['entity_type'],
            pk=self.kwargs['pk']
        )

        # O cache é visto somente aqui, para garantir que
        # não bypasse as permissões
        cache = get_cache(DATA_ENTITY_KEY_PREFIX, kwargs)
        if cache:
            return cache

        data = DadoEntidadeSerializer(
            obj,
            domain_id=self.kwargs['domain_id']
        ).data
        if not data['external_data']:
            raise Http404

        if obj.is_cacheable:
            save_cache(
                data,
                DATA_ENTITY_KEY_PREFIX,
                DATA_ENTITY_KEY_CHECK,
                kwargs
            )

        return Response(data)


class DadoDetalheView(RetrieveAPIView):
    serializer_class = DadoDetalheSerializer

    def get(self, request, *args, **kwargs):
        permissions = get_permissions(request)

        obj = get_object_or_404(
            DadoDetalhe.objects.get_authorized(permissions),
            dado_main__entity_type__abreviation=self.kwargs['entity_type'],
            pk=self.kwargs['pk']
        )

        # O cache é visto somente aqui, para garantir que
        # não bypasse as permissões
        cache = get_cache(DATA_DETAIL_KEY_PREFIX, kwargs)
        if cache:
            return cache

        data = DadoDetalheSerializer(
            obj,
            domain_id=self.kwargs['domain_id']
        ).data
        if not data['external_data']:
            raise Http404

        if obj.is_cacheable:
            save_cache(
                data,
                DATA_DETAIL_KEY_PREFIX,
                DATA_DETAIL_KEY_CHECK,
                kwargs
            )

        return Response(data)


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
