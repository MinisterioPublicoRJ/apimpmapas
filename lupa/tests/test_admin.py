from django.contrib.admin.sites import AdminSite
from model_mommy.mommy import make
from unittest import TestCase, mock
from lupa.admin import remove_data_from_cache, remove_entity_from_cache
from lupa.models import DadoEntidade
from lupa.admin import DadoEntidadeAdmin
import pytest


@pytest.mark.django_db(transaction=True)
class TestMoveDadoToPosition(TestCase):
    def setUp(self):
        self.adminsite = AdminSite()
        self.dadoadmin = DadoEntidadeAdmin(
            DadoEntidade,
            self.adminsite
        )

    def test_correct_render(self):
        request = mock.MagicMock()
        dado = make(
            'lupa.DadoEntidade',
            title="Este Dado",
            order=4
        )

        queryset = [dado]

        response = self.dadoadmin.move_dado_to_position(
            request,
            queryset
        )

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertIn(
            b'input type="hidden" name="action" value="move_dado_to_position"',
            response.content
        )
        self.assertIn(
            b'Para qual posi\xc3\xa7\xc3\xa3o '
            b'voc\xc3\xaa deseja mover Este Dado?',
            response.content
        )
        self.assertIn(
            b'<input type="hidden" name="_selected_action" value="1" />',
            response.content
        )

    @mock.patch.object(DadoEntidadeAdmin, 'message_user')
    @mock.patch.object(DadoEntidade, 'to')
    def test_input_move(self, _to, _msu):
        dado = make(
            'lupa.DadoEntidade',
            title="Este Dado",
            order=4
        )

        queryset = [dado]

        request = mock.MagicMock()
        request.POST = {
            'apply': True,
            'new_order': 14,
        }

        request.get_full_path = mock.MagicMock()
        request.get_full_path.side_effect = "path/to/url"

        response = self.dadoadmin.move_dado_to_position(
            request,
            queryset
        )

        self.assertEqual(
            response.status_code,
            302
        )
        _to.assert_called_once_with(14)
        _msu.assert_called_once_with(
            request,
            'Atualizei a ordem da caixinha Este Dado'
        )


@pytest.mark.django_db(transaction=True)
class ClearFromCache(TestCase):
    @mock.patch('lupa.admin.django_cache')
    def test_clear_data_from_cache(self, _django_cache):
        rd_mock = mock.MagicMock()
        rd_mock.keys.side_effect = [
            ['key 1.1', 'key 1.2'],
            ['key 2.1', 'key 2.2']
        ]
        _django_cache.get_master_client.return_value = rd_mock
        modeladmin = None
        request = None

        dado_1 = make(
            'lupa.DadoEntidade',
        )
        dado_2 = make(
            'lupa.DadoEntidade',
        )

        queryset = [dado_1, dado_2]

        remove_data_from_cache(modeladmin, request, queryset)

        key_prefix = 'lupa_dado'
        rd_keys_calls = [
            mock.call(
                '*%s:%s:*:%s'
                % (key_prefix, dado_1.entity_type.abreviation, dado_1.pk)
            ),
            mock.call(
                '*%s:%s:*:%s'
                % (key_prefix, dado_2.entity_type.abreviation, dado_2.pk)
            )
        ]

        rd_delete_calls = [
            mock.call('key 1.1'),
            mock.call('key 1.2'),
            mock.call('key 2.1'),
            mock.call('key 2.2')
        ]

        _django_cache.get_master_client.assert_called_once_with()
        rd_mock.keys.assert_has_calls(rd_keys_calls)
        rd_mock.delete.assert_has_calls(rd_delete_calls)

    @mock.patch('lupa.admin.django_cache')
    def test_clear_entity_from_cache(self, _django_cache):
        rd_mock = mock.MagicMock()
        rd_mock.keys.side_effect = [
            ['key 1.1', 'key 1.2'],
            ['key 2.1', 'key 2.2']
        ]
        _django_cache.get_master_client.return_value = rd_mock
        modeladmin = None
        request = None

        entidade_1 = make(
            'lupa.Entidade',
        )
        entidade_2 = make(
            'lupa.Entidade',
        )

        queryset = [entidade_1, entidade_2]

        remove_entity_from_cache(modeladmin, request, queryset)

        key_prefix = 'lupa_entidade'
        rd_keys_calls = [
            mock.call(
                '*%s:%s:*'
                % (key_prefix, entidade_1.abreviation)
            ),
            mock.call(
                '*%s:%s:*'
                % (key_prefix, entidade_2.abreviation)
            )
        ]

        rd_delete_calls = [
            mock.call('key 1.1'),
            mock.call('key 1.2'),
            mock.call('key 2.1'),
            mock.call('key 2.2')
        ]

        _django_cache.get_master_client.assert_called_once_with()
        rd_mock.keys.assert_has_calls(rd_keys_calls)
        rd_mock.delete.assert_has_calls(rd_delete_calls)
