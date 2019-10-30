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

from lupa.cache import custom_cache
from .models import Entidade, DadoDetalhe, DadoEntidade
from .serializers import (
    EntidadeSerializer,
    DadoDetalheSerializer,
    DadoEntidadeSerializer,
    EntidadeIdSerializer
)
from .osmapi import query as osmquery
from .db_connectors import execute_geospatial


class EntityDataView:
    def process_request(self, request, obj, serializer, key_check):
        if isinstance(obj, (Entidade, DadoEntidade)):
            roles = obj.roles_allowed.all().values_list('role', flat=True)
        elif isinstance(obj, DadoDetalhe):
            roles = obj.dado_main.roles_allowed.all().values_list(
                'role',
                flat=True
            )
        else:
            return Response({}, status=401)
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

    @custom_cache(
        key_prefix='lupa_entidade',
        model_kwargs={'abreviation': 'entity_type'}
    )
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            abreviation=self.kwargs['entity_type']
        )

        response = self.process_request(
            request,
            obj,
            EntidadeSerializer,
            'exibition_field'

        )
        return response


class DadoEntidadeView(RetrieveAPIView, EntityDataView):
    serializer_class = DadoEntidadeSerializer
    queryset = DadoEntidade.objects.all()

    @custom_cache(
        key_prefix='lupa_dado_entidade',
        model_kwargs={'entity_type__abreviation': 'entity_type', 'pk': 'pk'}
    )
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            entity_type__abreviation=self.kwargs['entity_type'],
            pk=self.kwargs['pk']
        )

        return self.process_request(
            request,
            obj,
            DadoEntidadeSerializer,
            'external_data'
        )


class DadoDetalheView(RetrieveAPIView, EntityDataView):
    serializer_class = DadoDetalheSerializer
    queryset = DadoDetalhe.objects.all()

    @custom_cache(
        key_prefix='lupa_dado_detalhe',
        model_kwargs={
            'dado_main__entity_type__abreviation': 'entity_type',
            'pk': 'pk'
        }
    )
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            dado_main__entity_type__abreviation=self.kwargs['entity_type'],
            pk=self.kwargs['pk']
        )

        return self.process_request(
            request,
            obj,
            DadoDetalheSerializer,
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
