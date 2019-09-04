from functools import wraps

import jwt

from rest_framework.response import Response
from decouple import config
from jwt.exceptions import InvalidSignatureError, DecodeError


def auth_required(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        request = args[1]
        token = request.GET.get('auth_token')

        try:
            token = jwt.decode(
                token,
                config('SECRET_KEY'),
                algorithms=["HS256"]
            )
            return func(*args, **kwargs)
        except (InvalidSignatureError, DecodeError):
            return Response({}, status=403)

    return inner_func
