from unittest import TestCase, mock

from lupa.tasks import (
    asynch_repopulate_cache_entity,
    asynch_repopulate_cache_data_entity,
    asynch_repopulate_cache_data_detail,
    asynch_remove_from_cache)


class Task(TestCase):
    @mock.patch('lupa.tasks._repopulate_cache_entity')
    def test_call_repopulate_cache_entity(self, _rep_cache):
        asynch_repopulate_cache_entity(
            key_prefix='lupa_entidade',
            queryset=None,
            serializer=None
        )

        _rep_cache.assert_called_once_with('lupa_entidade', None, None)

    @mock.patch('lupa.tasks._repopulate_cache_data_entity')
    def test_call_repopulate_cache_data_entity(self, _rep_cache):
        queryset_mock = mock.MagicMock()
        asynch_repopulate_cache_data_entity(
            key_prefix='lupa_dado_entidade',
            queryset=queryset_mock,
            serializer=None
        )

        _rep_cache.assert_called_once_with(
            'lupa_dado_entidade',
            queryset_mock,
            None
        )

    @mock.patch('lupa.tasks._repopulate_cache_data_detail')
    def test_call_repopulate_cache_data_detail(self, _rep_cache):
        queryset_mock = mock.MagicMock()
        asynch_repopulate_cache_data_detail(
            key_prefix='lupa_dado_detalhe',
            queryset=queryset_mock,
            serializer=None
        )

        _rep_cache.assert_called_once_with(
            'lupa_dado_detalhe',
            queryset_mock,
            None
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
