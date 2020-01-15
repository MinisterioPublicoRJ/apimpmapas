from unittest import TestCase, mock

from lupa.cache import (
    ENTITY_KEY_PREFIX,
    DATA_ENTITY_KEY_PREFIX,
    DATA_DETAIL_KEY_PREFIX
)
from lupa.tasks import (
    asynch_repopulate_cache_entity,
    asynch_repopulate_cache_data_entity,
    asynch_repopulate_cache_data_detail,
    asynch_remove_from_cache)


class Task(TestCase):
    @mock.patch('lupa.tasks._repopulate_cache_entity')
    def test_call_repopulate_cache_entity(self, _rep_cache):
        asynch_repopulate_cache_entity(
            key_prefix=ENTITY_KEY_PREFIX,
            queryset=None
        )

        _rep_cache.assert_called_once_with(ENTITY_KEY_PREFIX, None)

    @mock.patch('lupa.tasks._repopulate_cache_data_entity')
    def test_call_repopulate_cache_data_entity(self, _rep_cache):
        queryset_mock = mock.MagicMock()
        asynch_repopulate_cache_data_entity(
            key_prefix=DATA_ENTITY_KEY_PREFIX,
            queryset=queryset_mock
        )

        _rep_cache.assert_called_once_with(
            DATA_ENTITY_KEY_PREFIX,
            queryset_mock,
        )

    @mock.patch('lupa.tasks._repopulate_cache_data_detail')
    def test_call_repopulate_cache_data_detail(self, _rep_cache):
        queryset_mock = mock.MagicMock()
        asynch_repopulate_cache_data_detail(
            key_prefix=DATA_DETAIL_KEY_PREFIX,
            queryset=queryset_mock
        )

        _rep_cache.assert_called_once_with(
            DATA_DETAIL_KEY_PREFIX,
            queryset_mock,
        )

    @mock.patch('lupa.tasks._remove_from_cache')
    def test_call_remove_from_cache(self, _remove):
        queryset_mock = mock.MagicMock()
        model_args = ['args']
        asynch_remove_from_cache(
            'key_prefix',
            model_args,
            queryset_mock
        )

        _remove.assert_called_once_with(
            'key_prefix',
            model_args,
            queryset_mock,
        )
