from django.core.cache import cache as django_cache
from rest_framework.response import Response


def cache_key(key_prefix, kwargs):
    kwargs_key = ':'.join(
        str(val) for val in kwargs.values()
    )

    return '%s:%s' % (key_prefix, kwargs_key)


def custom_cache(timeout=None, key_prefix=None):
    key_prefix = '' if key_prefix is None else key_prefix

    def _custom_cache(func):
        def inner(*args, **kwargs):
            key = cache_key(key_prefix, kwargs)
            if key in django_cache:
                response_data = django_cache.get(key)
                return Response(response_data)

            response = func(*args, **kwargs)
            django_cache.set(key, response.data)
            return response

        return inner

    return _custom_cache
