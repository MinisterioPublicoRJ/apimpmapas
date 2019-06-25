import jwt

from decouple import config
from rest_framework.response import Response
from rest_framework.views import APIView

from login.sca import authenticate
from login.decorators import auth_required


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        sca_response = authenticate(username, password)

        if sca_response == 200:
            payload = {
                'uid': username
            }
            secret = config('SECRET_KEY')
            token = jwt.encode(payload, secret)
            return Response(token, status=200)

        return Response('Usuário ou senha incorretos', status=403)


class TestView(APIView):

    @auth_required
    def get(self, request, *args, **kwargs):
        return Response('Usuário Logado', status=200)
