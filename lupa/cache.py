from django.core.cache import cache as django_cache
from rest_framework.response import Response


def cache_key(key_prefix, kwargs):
    kwargs_key = ':'.join(
        str(val) for val in kwargs.values()
    )

    return '%s:%s' % (key_prefix, kwargs_key)


def custom_cache(func=None, timeout=300, key_args=['entity_type'],
                 key_prefix=''):

    def _custom_cache(func):

        def wrapper(*args, **kwargs):
            request = args[1]
            token = request.GET.get('auth_token', '')
            hash_key = cache_key(key_args, kwargs, token, key_prefix)

            if hash_key in django_cache:
                data = django_cache.get(hash_key)
                return Response(data)

            response = func(*args, **kwargs)
            django_cache.set(hash_key, response.data, timeout=timeout)

            return response

        return wrapper

    return _custom_cache
