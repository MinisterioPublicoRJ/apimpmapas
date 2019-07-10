from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.models import Entidade, Dado
from api.serializers import EntidadeSerializer, DadoSerializer


class EntidadeView(GenericAPIView):
    serializer_class = EntidadeSerializer
    queryset = Entidade.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.queryset,
            entity_type=self.kwargs['entity_type'],
            domain_id=self.kwargs['domain_id']
        )

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response(EntidadeSerializer(
            obj,
            entity_type=self.kwargs['entity_type']
        ).data)


class DadoView(RetrieveAPIView):
    serializer_class = DadoSerializer
    queryset = Dado.objects.all()

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            entity_type=self.kwargs['entity_type'],
            pk=self.kwargs['pk']
        )

        data = DadoSerializer(obj, domain_id=self.kwargs['domain_id']).data
        if not data['external_data']:
            raise Http404
        return Response(data)
