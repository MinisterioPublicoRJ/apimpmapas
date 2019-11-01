from lupa.cache import (
    _repopulate_cache_entity,
    _repopulate_cache_data_entity,
    _repopulate_cache_data_detail,
    _remove_from_cache
)

from mprj_api.celeryconfig import app


@app.task
def asynch_repopulate_cache_entity(key_prefix, queryset, serializer):
    _repopulate_cache_entity(key_prefix, queryset, serializer)


@app.task
def asynch_repopulate_cache_data_entity(key_prefix, queryset, serializer):
    _repopulate_cache_data_entity(key_prefix, queryset, serializer)


@app.task
def asynch_repopulate_cache_data_detail(key_prefix, queryset, serializer):
    _repopulate_cache_data_detail(key_prefix, queryset, serializer)


@app.task
def asynch_remove_from_cache(key_prefix, model_args, queryset):
    _remove_from_cache(key_prefix, model_args, queryset)
