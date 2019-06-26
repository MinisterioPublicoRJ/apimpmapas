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
            jwt.decode(
                token,
                config('SECRET_KEY'),
                algorithms=["HS256"]
            )
        except (InvalidSignatureError, DecodeError):
            return Response({}, status=403)

        return func(*args, **kwargs)

    return inner_func
