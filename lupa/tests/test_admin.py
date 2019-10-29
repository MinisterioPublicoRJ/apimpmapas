from django.contrib.admin.sites import AdminSite
from model_mommy.mommy import make
from unittest import TestCase, mock
from lupa.admin import remove_data_from_cache, remove_entity_from_cache
from lupa.models import DadoEntidade, DadoDetalhe
from lupa.admin import DadoEntidadeAdmin
from lupa.serializers import (EntidadeSerializer,
                              DadoEntidadeSerializer,
                              DadoDetalheSerializer)
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
    @mock.patch('lupa.admin.asynch_repopulate_cache_data_detail')
    @mock.patch('lupa.admin.asynch_repopulate_cache_data_entity')
    @mock.patch('lupa.admin.django_cache')
    def test_clear_data_from_cache(self,
                                   _django_cache, asynch_rep_data_entity,
                                   asynch_rep_data_detail):

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

        key_prefix = 'lupa_dado_entidade'
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
        asynch_rep_data_entity.delay.assert_called_once_with(
            key_prefix,
            queryset,
            DadoEntidadeSerializer
        )

    @mock.patch('lupa.admin.asynch_repopulate_cache_data_detail')
    @mock.patch('lupa.admin.asynch_repopulate_cache_data_entity')
    @mock.patch('lupa.admin.django_cache')
    def test_clear_data_and_its_detail_from_cache(
        self,
        _django_cache,
        asynch_rep_cache_data_entity,
        asynch_rep_cache_data_detail
    ):

        rd_mock = mock.MagicMock()
        rd_mock.keys.side_effect = [
            ['key entidade 1.1', 'key entidade 1.2'],
            ['key entidade 2.1', 'key entidade 2.2'],
            ['key detalhe 1.1', 'key detalhe 1.2'],
            ['key detalhe 2.1', 'key detalhe 2.2'],
            ['key detalhe 3.1', 'key detalhe 3.2'],
            ['key detalhe 4.1', 'key detalhe 4.2'],
        ]
        _django_cache.get_master_client.return_value = rd_mock
        modeladmin = None
        request = None

        dado_entidade_1 = make(
            'lupa.DadoEntidade',
        )
        dado_entidade_2 = make(
            'lupa.DadoEntidade',
        )
        # Thist entity wasn't selected in Admin
        dado_entidade_3 = make(
            'lupa.DadoEntidade',
        )
        dado_detalhe_1_1 = make(
            'lupa.DadoDetalhe',
            dado_main=dado_entidade_1
        )
        dado_detalhe_1_2 = make(
            'lupa.DadoDetalhe',
            dado_main=dado_entidade_1
        )
        dado_detalhe_2_1 = make(
            'lupa.DadoDetalhe',
            dado_main=dado_entidade_2
        )
        dado_detalhe_2_2 = make(
            'lupa.DadoDetalhe',
            dado_main=dado_entidade_2
        )
        make(
            'lupa.DadoDetalhe',
            dado_main=dado_entidade_3
        )

        # Only dado_entidade_1 and dado_entidade_2 weere 'selected' in admin
        queryset = [dado_entidade_1, dado_entidade_2]

        remove_data_from_cache(modeladmin, request, queryset)

        key_prefix_entidade = 'lupa_dado_entidade'
        key_prefix_detalhe = 'lupa_dado_detalhe'
        rd_keys_calls = [
            mock.call(
                '*%s:%s:*:%s'
                % (
                    key_prefix_entidade,
                    dado_entidade_1.entity_type.abreviation,
                    dado_entidade_1.pk
                )
            ),
            mock.call(
                '*%s:%s:*:%s'
                % (
                    key_prefix_entidade,
                    dado_entidade_2.entity_type.abreviation,
                    dado_entidade_2.pk
                )
            ),
            mock.call(
                '*%s:%s:*:%s'
                % (
                    key_prefix_detalhe,
                    dado_detalhe_1_1.dado_main.entity_type.abreviation,
                    dado_detalhe_1_1.pk
                )
            ),
            mock.call(
                '*%s:%s:*:%s'
                % (
                    key_prefix_detalhe,
                    dado_detalhe_1_2.dado_main.entity_type.abreviation,
                    dado_detalhe_1_2.pk
                )
            ),
            mock.call(
                '*%s:%s:*:%s'
                % (
                    key_prefix_detalhe,
                    dado_detalhe_2_1.dado_main.entity_type.abreviation,
                    dado_detalhe_2_1.pk
                )
            ),
            mock.call(
                '*%s:%s:*:%s'
                % (
                    key_prefix_detalhe,
                    dado_detalhe_2_2.dado_main.entity_type.abreviation,
                    dado_detalhe_2_2.pk
                )
            ),
        ]

        rd_delete_calls = [
            mock.call('key entidade 1.1'),
            mock.call('key entidade 1.2'),
            mock.call('key entidade 2.1'),
            mock.call('key entidade 2.2'),
            mock.call('key detalhe 1.1'),
            mock.call('key detalhe 1.2'),
            mock.call('key detalhe 2.1'),
            mock.call('key detalhe 2.2'),
            mock.call('key detalhe 3.1'),
            mock.call('key detalhe 3.2'),
            mock.call('key detalhe 4.1'),
            mock.call('key detalhe 4.2'),
        ]
        expected_queryset = list(DadoDetalhe.objects.filter(
            dado_main__id__in=[d.id for d in queryset]
        ).order_by('pk').values_list('id'))

        _django_cache.get_master_client.assert_called_once_with()
        rd_mock.keys.assert_has_calls(rd_keys_calls)
        rd_mock.delete.assert_has_calls(rd_delete_calls)
        asynch_rep_cache_data_entity.delay.assert_called_once_with(
            key_prefix_entidade,
            queryset,
            DadoEntidadeSerializer
        )
        call_args = asynch_rep_cache_data_detail.delay.call_args_list[0][0]
        self.assertEqual(call_args[0], key_prefix_detalhe)
        self.assertEqual(
            list(call_args[1].values_list('id')),
            expected_queryset
        )
        self.assertEqual(call_args[2], DadoDetalheSerializer)

    @mock.patch('lupa.admin.asynch_repopulate_cache_entity')
    @mock.patch('lupa.admin.django_cache')
    def test_clear_entity_from_cache(self, _django_cache, asynch_rep_cache):
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
        asynch_rep_cache.delay.assert_called_once_with(
            key_prefix,
            queryset,
            EntidadeSerializer
        )
