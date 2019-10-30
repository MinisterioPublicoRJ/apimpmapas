from unittest import TestCase, mock

from lupa.tasks import (
    asynch_repopulate_cache_entity,
    asynch_repopulate_cache_data_entity,
    asynch_repopulate_cache_data_detail)


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
