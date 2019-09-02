from rest_framework import viewsets

from .models import Area, Tema, Icone
from .serializers import AreaSerializer, TemaSerializer, IconeSerializer


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class TemaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tema.objects.filter(visivel=True)
    serializer_class = TemaSerializer


class IconeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Icone.objects.all()
    serializer_class = IconeSerializer
