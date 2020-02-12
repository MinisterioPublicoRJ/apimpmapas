from rest_framework.response import Response
from rest_framework.views import APIView


class DesaparecidosView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({}, status=200)
