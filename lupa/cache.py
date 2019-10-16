from hashlib import md5


def cache_key(args_list, kwargs, token):
    ctx = md5()
    for arg in args_list:
        ctx.update(str(kwargs[arg]).encode('ascii'))

    token_ctx = md5(str(token).encode('ascii'))
    return '%s_%s' % (ctx.hexdigest(), token_ctx.hexdigest())
