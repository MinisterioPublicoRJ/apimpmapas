from functools import partial, wraps

from django.conf import settings
from django.core.exceptions import PermissionDenied


def token_required(
        fun=None, *, token_conf_var="token-conf-var", name="token"
):
    if fun is None:
        return partial(
            token_required,
            token_conf_var=token_conf_var,
            name=name
        )

    @wraps(fun)
    def wrapper(*args, **kwargs):
        request = args[1]
        token = request.GET.get(name)
        if token != getattr(settings, token_conf_var, None):
            raise PermissionDenied("Token incorreto ou inexistente!")

        return fun(*args, **kwargs)

    return wrapper
