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
    @mock.patch('lupa.admin.chain')
    @mock.patch('lupa.admin.asynch_repopulate_cache_data_detail')
    @mock.patch('lupa.admin.asynch_repopulate_cache_data_entity')
    @mock.patch('lupa.admin.asynch_remove_from_cache')
    def test_clear_data_from_cache(self,
                                   asynch_remove,
                                   asynch_rep_data_entity,
                                   asynch_rep_data_detail,
                                   _chain):

        flow_mock = mock.MagicMock()
        _chain.return_value = flow_mock

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

        entity_key_prefix = 'lupa_dado_entidade'
        detail_key_prefix = 'lupa_dado_detalhe'

        self.assertEqual(
            asynch_remove.si.call_args_list[0][0][0],
            entity_key_prefix
        )
        self.assertEqual(
            asynch_remove.si.call_args_list[0][0][1],
            ['entity_type.abreviation', 'pk'],
        )
        self.assertEqual(
            asynch_remove.si.call_args_list[0][0][2],
            queryset
        )
        self.assertEqual(
            asynch_remove.si.call_args_list[1][0][0],
            detail_key_prefix
        )
        self.assertEqual(
            asynch_remove.si.call_args_list[1][0][1],
            ['dado_main.entity_type.abreviation', 'pk'],
        )
        self.assertEqual(
            asynch_remove.si.call_args_list[0][0][1],
            ['entity_type.abreviation', 'pk'],
            []
        )
        asynch_rep_data_entity.si.assert_called_once_with(
            entity_key_prefix,
            queryset,
            DadoEntidadeSerializer
        )
        self.assertEqual(_chain.call_args_list[0][0][0], asynch_remove.si())
        self.assertEqual(
            _chain.call_args_list[0][0][1], asynch_rep_data_entity.si()
        )
        flow_mock.delay.assert_has_calls([mock.call(), mock.call()])

    @mock.patch('lupa.admin.chain')
    @mock.patch('lupa.admin.asynch_repopulate_cache_data_detail')
    @mock.patch('lupa.admin.asynch_repopulate_cache_data_entity')
    @mock.patch('lupa.admin.asynch_remove_from_cache')
    def test_clear_data_and_its_detail_from_cache(
        self,
        asynch_remove_data,
        asynch_rep_cache_data_entity,
        asynch_rep_cache_data_detail,
        _chain
    ):

        flow_mock = mock.MagicMock()
        _chain.return_value = flow_mock
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
        make(
            'lupa.DadoDetalhe',
            dado_main=dado_entidade_1
        )
        make(
            'lupa.DadoDetalhe',
            dado_main=dado_entidade_1
        )
        make(
            'lupa.DadoDetalhe',
            dado_main=dado_entidade_2
        )
        make(
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
        expected_queryset = list(DadoDetalhe.objects.filter(
            dado_main__id__in=[d.id for d in queryset]
        ).order_by('pk').values_list('id'))

        key_prefix_entidade = 'lupa_dado_entidade'
        key_prefix_detalhe = 'lupa_dado_detalhe'

        self.assertEqual(
            asynch_rep_cache_data_entity.si.call_args_list[0][0][0],
            key_prefix_entidade
        )
        self.assertEqual(
            asynch_rep_cache_data_entity.si.call_args_list[0][0][1],
            queryset
        )
        self.assertEqual(
            asynch_rep_cache_data_entity.si.call_args_list[0][0][2],
            DadoEntidadeSerializer
        )
        asynch_rep_cache_data_entity.si.assert_called_once_with(
            key_prefix_entidade,
            queryset,
            DadoEntidadeSerializer
        )
        call_args = asynch_rep_cache_data_detail.si.call_args_list[0][0]
        self.assertEqual(call_args[0], key_prefix_detalhe)
        self.assertEqual(
            list(call_args[1].values_list('id')),
            expected_queryset
        )
        self.assertEqual(call_args[2], DadoDetalheSerializer)
        self.assertEqual(
            _chain.call_args_list[0][0][0],
            asynch_remove_data.si()
        )
        self.assertEqual(
            _chain.call_args_list[0][0][1],
            asynch_rep_cache_data_entity.si()
        )
        self.assertEqual(
            _chain.call_args_list[1][0][0],
            asynch_remove_data.si()
        )
        self.assertEqual(
            _chain.call_args_list[1][0][1],
            asynch_rep_cache_data_detail.si()
        )
        flow_mock.delay.assert_has_calls([mock.call(), mock.call()])

    @mock.patch('lupa.admin.chain')
    @mock.patch('lupa.admin.asynch_repopulate_cache_entity')
    @mock.patch('lupa.admin.asynch_remove_from_cache')
    def test_clear_entity_from_cache(self, asynch_remove, asynch_rep_cache,
                                     _chain):
        flow_mock = mock.MagicMock()
        _chain.return_value = flow_mock
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

        asynch_remove.si.assert_called_once_with(
            key_prefix,
            ['abreviation'],
            queryset,
        )
        asynch_rep_cache.si.assert_called_once_with(
            key_prefix,
            queryset,
            EntidadeSerializer
        )
        _chain.assert_called_once_with(
            asynch_remove.si(),
            asynch_rep_cache.si()
        )
        flow_mock.delay.assert_called_once_with()
