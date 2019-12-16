import jwt
from decouple import config
from jwt import InvalidSignatureError, DecodeError


def get_permissions(request):
    token = request.GET.get('auth_token')
    try:
        payload = jwt.decode(
            token,
            config('SECRET_KEY'),
            algorithms=["HS256"]
        )
        return payload.get('permissions', [])
    except (InvalidSignatureError, DecodeError):
        return []
