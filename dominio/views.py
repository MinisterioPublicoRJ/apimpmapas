from rest_framework.generics import ListAPIView

from .models import Alerta  # implementar, e fazer trava no JWT
from .serializers import AlertaSerializer  # implementar


# Create your views here.
class AlertasListView(ListAPIView):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
