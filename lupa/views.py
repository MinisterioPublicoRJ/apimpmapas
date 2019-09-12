from decouple import config
from django.http import Http404
from django.shortcuts import get_object_or_404
import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    ListAPIView
)
from rest_framework.response import Response

from .models import Entidade, Dado
from .serializers import EntidadeSerializer, DadoSerializer
from .osmapi import query as osmquery


class EntidadeView(GenericAPIView):
    serializer_class = EntidadeSerializer
    queryset = Entidade.objects.all()

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            abreviation=self.kwargs['entity_type']
        )

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

        data = EntidadeSerializer(obj, domain_id=self.kwargs['domain_id']).data
        if not data['exibition_field']:
            raise Http404
        return Response(data)


class DadoView(RetrieveAPIView):
    serializer_class = DadoSerializer
    queryset = Dado.objects.all()

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            entity_type__abreviation=self.kwargs['entity_type'],
            pk=self.kwargs['pk']
        )

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

        data = DadoSerializer(obj, domain_id=self.kwargs['domain_id']).data
        if not data['external_data']:
            raise Http404
        return Response(data)


class OsmQueryView(ListAPIView):
    queryset = []

    def get(self, request, *args, **kwargs):
        return Response(osmquery(self.kwargs['terms']))
