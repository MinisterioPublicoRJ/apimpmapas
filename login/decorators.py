from functools import wraps

from decouple import config
import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError
from rest_framework.response import Response

from lupa.models import Dado


def auth_required(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        request = args[1]
        token = request.GET.get('auth_token')

        dado = Dado.objects.get(pk=kwargs['pk'])
        restricted_to = []
        for role in dado.roles_allowed.all().values_list('role', flat=True):
            restricted_to.append(role)

        if not restricted_to:
            return func(*args, **kwargs)

        try:
            token = jwt.decode(
                token,
                config('SECRET_KEY'),
                algorithms=["HS256"]
            )
            # TODO checagem de permissões
            # permissions = token['permissions']
            return func(*args, **kwargs)
        except (InvalidSignatureError, DecodeError):
            return Response({}, status=403)

    return inner_func
