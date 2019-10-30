from lupa.cache import (
    _repopulate_cache_entity,
    _repopulate_cache_data_entity,
    _repopulate_cache_data_detail
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
