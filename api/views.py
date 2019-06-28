from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.models import Entidade
from api.serializers import EntidadeSerializer


class EntidadeView(GenericAPIView):
    serializer_class = EntidadeSerializer
    queryset = Entidade.objects.all()

    def get_object(self):
        return self.queryset.get(
            entity_type__name=self.kwargs['entity_type'],
            domain_id=self.kwargs['domain_id']
        )

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response(EntidadeSerializer(obj).data)
