from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import Entidade, Dado
from .serializers import EntidadeSerializer, DadoSerializer
from login.decorators import auth_required


class EntidadeView(GenericAPIView):
    serializer_class = EntidadeSerializer
    queryset = Entidade.objects.all()

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            abreviation=self.kwargs['entity_type']
        )

        data = EntidadeSerializer(obj, domain_id=self.kwargs['domain_id']).data
        if not data['exibition_field']:
            raise Http404
        return Response(data)


class DadoView(RetrieveAPIView):
    serializer_class = DadoSerializer
    queryset = Dado.objects.all()

    @auth_required
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.queryset,
            entity_type__abreviation=self.kwargs['entity_type'],
            pk=self.kwargs['pk']
        )

        data = DadoSerializer(obj, domain_id=self.kwargs['domain_id']).data
        if not data['external_data']:
            raise Http404
        return Response(data)
