from hashlib import md5

from django.core.cache import cache as django_cache
from rest_framework.response import Response


def cache_key(args_list, kwargs, token, key_prefix):
    ctx = md5()
    for arg in args_list:
        ctx.update(str(kwargs[arg]).encode('ascii'))

    token_ctx = md5(str(token).encode('ascii'))
    return '%s_%s_%s' % (key_prefix, ctx.hexdigest(), token_ctx.hexdigest())


def custom_cache(func=None, timeout=300, key_prefix=''):
    def _custom_cache(func):
        def wrapper(*args, **kwargs):
            request = args[1]
            token = request.GET.get('auth_token', '')
            args_list = ['entity_type']
            hash_key = cache_key(args_list, kwargs, token, key_prefix)

            if hash_key in django_cache:
                data = django_cache.get(hash_key)
                return Response(data)

            response = func(*args, **kwargs)
            django_cache.set(hash_key, response.data, timeout=timeout)

            return response

        return wrapper

    return _custom_cache
