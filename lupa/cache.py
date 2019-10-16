from hashlib import md5

from django.core.cache import cache as django_cache


def cache_key(args_list, kwargs, token):
    ctx = md5()
    for arg in args_list:
        ctx.update(str(kwargs[arg]).encode('ascii'))

    token_ctx = md5(str(token).encode('ascii'))
    return '%s_%s' % (ctx.hexdigest(), token_ctx.hexdigest())


def custom_cache(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        token = request.GET.get('auth_token', '')
        args_list = ['entity_type']
        hash_key = cache_key(args_list, kwargs, token)
        response = func(*args, **kwargs)
        django_cache.set(hash_key, response.data)

        return response

    return wrapper
