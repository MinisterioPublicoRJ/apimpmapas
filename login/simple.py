from functools import wraps

from django.conf import settings
from django.core.exceptions import PermissionDenied


def token_required(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        request = args[1]
        token = request.GET.get("proxy-token")
        if token != settings.SIMPLE_AUTH_TOKEN:
            raise PermissionDenied("Token incorreto ou inexistente!")

        return fun(*args, **kwargs)

    return wrapper
