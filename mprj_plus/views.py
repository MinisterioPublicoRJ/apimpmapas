from rest_framework import viewsets

from .models import Area, Tema
from .serializers import AreaSerializer, TemaSerializer


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class TemaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tema.objects.filter(visivel=True)
    serializer_class = TemaSerializer
