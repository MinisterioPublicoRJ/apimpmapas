import sys

import jwt

from decouple import config
from django.core.cache import cache as django_cache
from django.core.management.base import OutputWrapper
from django.shortcuts import get_object_or_404
from jwt.exceptions import InvalidSignatureError, DecodeError
from rest_framework.response import Response

from lupa.db_connectors import execute_sample

STDERR = OutputWrapper(sys.stderr)


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


def _repopulate_cache_entity(key_prefix, queryset, serializer):
    entities = queryset.distinct('abreviation').order_by('abreviation')
    repopulate_cache(key_prefix, entities, queryset, serializer)


def _repopulate_cache_data_entity(key_prefix, queryset, serializer):
    entities = queryset.distinct('entity_type__abreviation').order_by(
        'entity_type__abreviation'
    )
    entities = [e.entity_type for e in entities]
    repopulate_cache(key_prefix, entities, queryset, serializer)


def _repopulate_cache_data_detail(key_prefix, queryset, serializer):
    entities = queryset.distinct(
        'dado_main__entity_type__abreviation').order_by(
            'dado_main__entity_type__abreviation'
    )
    entities = [e.dado_main.entity_type for e in entities]
    repopulate_cache(key_prefix, entities, queryset, serializer)


def _stderr(entity, domain_id):
    msg = 'NOK - %s' % ' - '.join(
        [entity.database,
         entity.schema,
         entity.table,
         entity.id_column,
         domain_id
         ]
    )
    STDERR.write(msg)


def repopulate_cache(key_prefix, entities, queryset, serializer):
    for entity in entities:
        # Temporary workaround
        if key_prefix == 'lupa_dado_entidade':
            objs = queryset.filter(entity_type=entity)
        elif key_prefix == 'lupa_dado_detalhe':
            objs = queryset.filter(dado_main__entity_type=entity)
        else:
            objs = queryset.filter(abreviation=entity.abreviation)

        domain_ids = execute_sample(
            entity.database,
            entity.schema,
            entity.table,
            [entity.id_column],
            limit=False
        )

        for obj in objs:
            for domain_id in domain_ids:
                try:
                    json_data = serializer(obj, domain_id=domain_id).data
                except Exception:
                    _stderr(entity, domain_id[0])
                    continue

                key_kwargs = {
                        'entity_type': entity.abreviation,
                        'domain_id': domain_id[0],
                }
                if key_prefix in ('lupa_dado_entidade', 'lupa_dado_detalhe'):
                    key_kwargs['pk'] = obj.pk

                key = cache_key(
                    key_prefix,
                    key_kwargs
                )
                django_cache.set(key, json_data, timeout=obj.cache_timeout)
