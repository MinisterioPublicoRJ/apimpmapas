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

ENTITY_KEY_CHECK = 'exibition_field'
DATA_ENTITY_KEY_CHECK = DATA_DETAIL_KEY_CHECK = 'external_data'

ENTITY_MODEL_KWARGS = {'abreviation': 'entity_type'}
DATA_ENTITY_MODEL_KWARGS = {
    'entity_type__abreviation': 'entity_type', 'pk': 'pk'
}
DATA_DETAIL_MODEL_KWARGS = {
    'dado_main__entity_type__abreviation': 'entity_type', 'pk': 'pk'
}


def wrap_response(response_data, key_check):
    status, data = (200, response_data) if response_data.get(key_check)\
        else (404, {"detail": "Não encontrado."})

    return {'data': data, 'status_code': status}


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


def cache_key(key_prefix, args_dict):
    kwargs_key = ':'.join(
        str(val) for val in args_dict.values()
    )

    return '%s:%s' % (key_prefix, kwargs_key)


def wildcard_cache_key(key_prefix, keys):
    wildcard_pos = 1
    keys = keys[:wildcard_pos] + ['*'] + keys[wildcard_pos:]
    kwargs_key = ':'.join(
        str(val) for val in keys
    )

    return '*%s:%s' % (key_prefix, kwargs_key)


def get_cache(obj, key_prefix, request_args):
    key = cache_key(key_prefix, request_args)
    if key in django_cache:
        cache_response = django_cache.get(key)
        return Response(
            cache_response['data'],
            status=cache_response['status_code']
        )


def save_cache(data, key_prefix, key_check, request_args):
    key = cache_key(key_prefix, request_args)
    wrapped_response = wrap_response(data, key_check)
    django_cache.set(key, wrapped_response, timeout=None)


def _repopulate_cache_entity(key_prefix, queryset):
    from lupa.serializers import EntidadeSerializer
    entities = queryset.distinct('abreviation').order_by('abreviation')
    key_check = 'exibition_field'
    repopulate_cache(
        key_prefix,
        entities,
        queryset,
        EntidadeSerializer,
        key_check
    )


def _repopulate_cache_data_entity(key_prefix, queryset):
    from lupa.serializers import DadoEntidadeSerializer
    entities = queryset.distinct('entity_type__abreviation').order_by(
        'entity_type__abreviation'
    )
    key_check = 'external_data'
    entities = [e.entity_type for e in entities]
    repopulate_cache(
        key_prefix,
        entities,
        queryset,
        DadoEntidadeSerializer,
        key_check
    )


def _repopulate_cache_data_detail(key_prefix, queryset):
    from lupa.serializers import DadoDetalheSerializer
    entities = queryset.distinct(
        'dado_main__entity_type__abreviation').order_by(
            'dado_main__entity_type__abreviation'
    )
    key_check = 'external_data'
    entities = [e.dado_main.entity_type for e in entities]
    repopulate_cache(
        key_prefix,
        entities,
        queryset,
        DadoDetalheSerializer,
        key_check
    )


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


def repopulate_cache(key_prefix, entities, queryset, serializer, key_check):
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
                    cache_data = serializer(obj, domain_id=domain_id[0]).data
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
                wrapped_response = wrap_response(cache_data, key_check)
                django_cache.set(
                    key,
                    wrapped_response,
                    timeout=obj.cache_timeout_sec
                )
                obj.last_cache_update = dt.date.today()
                # Set is_cacheable = True to avoid problems with the asynch
                # calls performed the 'save' method from obj
                obj.is_cacheable = True
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
