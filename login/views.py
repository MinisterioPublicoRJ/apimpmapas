from django.http import HttpResponse
from rest_framework.views import APIView

from login.sca import authenticate


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        sca_response = authenticate(username, password)

        if sca_response == 200:
            return HttpResponse('Logado')
