import jwt

from decouple import config
from django.core.cache import cache as django_cache
from django.shortcuts import get_object_or_404
from jwt.exceptions import InvalidSignatureError, DecodeError
from rest_framework.response import Response


def _decode_jwt(token):
    try:
        payload = jwt.decode(
            token,
            config('SECRET_KEY'),
            algorithms=["HS256"]
        )
        return payload.get('permissions', [])
    except (InvalidSignatureError, DecodeError):
        return []


def _has_role(obj, permissions):
    roles = obj.roles_allowed.all().values_list('role', flat=True)
    if roles:
        return [role for role in roles if role in permissions]

    return True


def cache_key(key_prefix, kwargs):
    kwargs_key = ':'.join(
        str(val) for val in kwargs.values()
    )

    return '%s:%s' % (key_prefix, kwargs_key)


def wildcard_cache_key(key_prefix, keys):
    wildcard_pos = 1
    keys = keys[:wildcard_pos] + ['*'] + keys[wildcard_pos:]
    kwargs_key = ':'.join(
        str(val) for val in keys
    )

    return '*%s:%s' % (key_prefix, kwargs_key)


def custom_cache(key_prefix, model_kwargs=dict()):
    def _custom_cache(func):
        def inner(*args, **kwargs):
            instance = args[0]
            request = args[1]
            obj = get_object_or_404(
                instance.queryset,
                **{k: kwargs[v] for k, v in model_kwargs.items()}
            )

            token = request.GET.get('auth_token')
            permissions = _decode_jwt(token)

            key = cache_key(key_prefix, kwargs)
            if key in django_cache and _has_role(obj, permissions):
                response_data = django_cache.get(key)
                return Response(response_data)

            response = func(*args, **kwargs)
            if response.status_code == 200 and obj.is_cacheable:
                django_cache.set(key, response.data, timeout=None)

            return response

        return inner

    return _custom_cache
