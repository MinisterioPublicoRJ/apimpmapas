from operator import attrgetter

import datetime as dt
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

ENTITY_KEY_PREFIX = 'lupa_entidade'
DATA_ENTITY_KEY_PREFIX = 'lupa_dado_entidade'
DATA_DETAIL_KEY_PREFIX = 'lupa_dado_detalhe'


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

            # If DadoDetalhe check role in the related DadoEntidade
            obj_role = obj
            if not hasattr(obj, 'roles_allowed'):
                obj_role = obj.dado_main

            token = request.GET.get('auth_token')
            permissions = _decode_jwt(token)

            key = cache_key(key_prefix, kwargs)
            if key in django_cache and _has_role(obj_role, permissions):
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
    query_args = {
        ENTITY_KEY_PREFIX: 'abreviation',
        DATA_ENTITY_KEY_PREFIX: 'entity_type__abreviation',
        DATA_DETAIL_KEY_PREFIX: 'dado_main__entity_type__abreviation'
    }
    for entity in entities:
        domain_ids = execute_sample(
            entity.database,
            entity.schema,
            entity.table,
            [entity.id_column],
            limit=False
        )

        objs = queryset.filter(**{query_args[key_prefix]: entity.abreviation})
        for obj in objs:
            for domain_id in domain_ids:
                try:
                    json_data = serializer(obj, domain_id=domain_id[0]).data
                except Exception:
                    _stderr(entity, domain_id[0])
                    continue

                key_kwargs = {
                        'entity_type': entity.abreviation,
                        'domain_id': domain_id[0],
                }
                if key_prefix in (DATA_ENTITY_KEY_PREFIX,
                                  DATA_DETAIL_KEY_PREFIX):
                    key_kwargs['pk'] = obj.pk

                key = cache_key(
                    key_prefix,
                    key_kwargs
                )
                django_cache.set(key, json_data, timeout=obj.cache_timeout_sec)
                obj.last_cache_update = dt.date.today()
                obj.save()


def _remove_from_cache(key_prefix, model_args, queryset):
    cache_client = django_cache.get_master_client()

    for obj in queryset:
        key_args = [
            attrgetter(arg)(obj) for arg in model_args
        ]
        key = wildcard_cache_key(key_prefix, key_args)
        cache_keys = cache_client.keys(key)
        [cache_client.delete(cache_key) for cache_key in cache_keys]
