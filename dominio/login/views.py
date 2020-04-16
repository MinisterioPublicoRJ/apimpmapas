from django.http import JsonResponse
from dominio.models import Usuario
from django.views.decorators.csrf import csrf_exempt

from .integra import authenticate_integra


@csrf_exempt
def login(request):
    response = authenticate_integra(request)
    usuario, created = Usuario.objects.get_or_create(
        username=response.get("username")
    )
    response["first_login"] = created
    response["first_login_today"] = created or usuario.get_first_login_today()
    usuario.save()

    return JsonResponse(response)
