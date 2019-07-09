import jwt

from decouple import config
from rest_framework.response import Response
from rest_framework.views import APIView

from login.sca import authenticate


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
            token = jwt.encode(payload, secret, algorithm="HS256")
            return Response(token, status=200)

        return Response('Usuário ou senha incorretos', status=403)
