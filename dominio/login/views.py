import login_sca
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from dominio.models import Usuario
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from .integra import authenticate_integra
from dominio.login import services


@csrf_exempt
def login_integra(request):
    "View responsável pela autenticação vinda do Integra"
    response = authenticate_integra(request)
    usuario, created = Usuario.objects.get_or_create(
        username=response.get("username")
    )
    response["first_login"] = created
    response["first_login_today"] = created or usuario.get_first_login_today()
    response["sexo"] = usuario.get_gender(response["matricula"])
    usuario.save()

    return JsonResponse(response)


class LoginPromotronView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        password = bytes(request.POST.get("password", ""), "utf-8")
        sca_resp = login_sca.login(
            username,
            password,
            settings.SCA_AUTH,
            settings.SCA_CHECK,
        )

        # TODO: maybe move this validation somewhere else.
        if sca_resp.auth.status_code != 200:
            raise PermissionDenied("Credenciais não encontradas")

        return Response(data=services.build_login_response(username))
