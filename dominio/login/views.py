import jwt
import login_sca
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from dominio.models import Usuario
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .integra import authenticate_integra
from dominio.login.arcgis import ARCGIS_TOKEN_CACHE_KEY
from dominio.login import services


@csrf_exempt
def login_integra(request):
    "View responsável pela autenticação vinda do Integra"
    try:
        response = authenticate_integra(request)
    except jwt.exceptions.DecodeError:
        return JsonResponse(
            {"erro": "Token inválido"}, status=HTTP_400_BAD_REQUEST
        )

    usuario, created = Usuario.objects.get_or_create(
        username=response.get("username")
    )
    response["first_login"] = created
    response["first_login_today"] = created or usuario.get_first_login_today()
    response["sexo"] = usuario.get_gender(response["matricula"])
    usuario.save()

    return JsonResponse(response)


class LoginView(APIView):
    def auth_sca(self, username, password):
        sca_resp = login_sca.login(
            username,
            password,
            settings.SCA_AUTH,
            settings.SCA_CHECK,
        )

        # TODO: maybe move this validation somewhere else.
        if sca_resp.auth.status_code != 200:
            raise PermissionDenied("Credenciais não encontradas")

        return sca_resp

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        password = bytes(request.POST.get("password", ""), "utf-8")

        sca_resp = self.auth_sca(username, password)
        permissoes = services.permissoes_router(sca_resp.info.json())

        return Response(data=services.build_login_response(permissoes))


class ArcGisTokenView(APIView):
    def get(self, request, *args, **kwargs):
        token_data = cache.get(ARCGIS_TOKEN_CACHE_KEY)
        return Response(data=token_data)
