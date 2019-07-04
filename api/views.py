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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            domain_id=self.kwargs['domain_id']
        )
        return Response(serializer.data)
