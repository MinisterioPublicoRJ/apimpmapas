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


from lupa.cache import (
    ENTITY_KEY_PREFIX,
    DATA_ENTITY_KEY_PREFIX,
    DATA_DETAIL_KEY_PREFIX
)
from lupa.tests.fixtures.admin import (
    entidade_name,
    dado_1_id,
    dado_1_title,
    dado_2_id,
    dado_2_title,
    dado_base_1_id,
    dado_base_1_title,
    dado_base_2_id,
    dado_base_2_title,
    hidden_field,
    html_list,
    id_fields,
    form_select,
)


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

        entity_key_prefix = DATA_ENTITY_KEY_PREFIX
        detail_key_prefix = DATA_DETAIL_KEY_PREFIX

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

        key_prefix_entidade = DATA_ENTITY_KEY_PREFIX
        key_prefix_detalhe = DATA_DETAIL_KEY_PREFIX

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

        key_prefix = ENTITY_KEY_PREFIX

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


@pytest.mark.django_db(transaction=True)
class TestChangeToDetail(TestCase):
    def setUp(self):
        self.adminsite = AdminSite()
        self.dadoadmin = DadoEntidadeAdmin(
            DadoEntidade,
            self.adminsite
        )

    def test_flatten_entities(self):
        entidade_1 = make('lupa.Entidade')
        entidade_2 = make('lupa.Entidade')
        make('lupa.DadoEntidade', entity_type=entidade_1)
        make('lupa.DadoEntidade', entity_type=entidade_2)

        queryset = DadoEntidade.objects.all()
        entidades = DadoEntidadeAdmin._get_entities(queryset)
        flatten = [entidade_1.name, entidade_2.name]

        self.assertCountEqual(entidades, flatten)

    @mock.patch('lupa.admin.messages')
    def test_validator(self, _msg):
        request = mock.MagicMock()
        entidades_true = ['a']
        entidades_error = ['a', 'b']

        message = (
            f'Foram selecionados dados de '
            f'{len(entidades_error)} entidades diferentes. '
            f'Selecione apenas dados de uma mesma entidade.'
        )

        valida_true = DadoEntidadeAdmin._valida_entidade_detailer(
            request, entidades_true
        )
        valida_false = DadoEntidadeAdmin._valida_entidade_detailer(
            request, entidades_error
        )

        self.assertTrue(valida_true)
        self.assertFalse(valida_false)
        _msg.error.assert_called_once_with(request, message)

    def test_render(self):
        request = mock.MagicMock()

        entidade = make('lupa.Entidade', name=entidade_name)
        make(
            'lupa.DadoEntidade',
            entity_type=entidade,
            id=dado_base_1_id,
            title=dado_base_1_title
        )
        make(
            'lupa.DadoEntidade',
            entity_type=entidade,
            id=dado_base_2_id,
            title=dado_base_2_title
        )
        make(
            'lupa.DadoEntidade',
            id=dado_1_id,
            entity_type=entidade,
            title=dado_1_title
        )
        make(
            'lupa.DadoEntidade',
            id=dado_2_id,
            entity_type=entidade,
            title=dado_2_title
        )

        queryset = DadoEntidade.objects.filter(id__in=[dado_1_id, dado_2_id])

        renderer = DadoEntidadeAdmin._render_changer(request, queryset)

        self.assertEqual(renderer.status_code, 200)
        content = renderer.content.decode('utf-8')

        self.assertIn(hidden_field, content)
        self.assertIn(html_list, content)
        self.assertIn(id_fields, content)
        self.assertIn(form_select, content)

    @mock.patch.object(DadoEntidadeAdmin, '_valida_entidade_detailer')
    def test_multiple_entities(self, _validator):
        request = mock.MagicMock()
        _validator.return_value = False

        entidade_1 = make('lupa.Entidade')
        entidade_2 = make('lupa.Entidade')
        make('lupa.DadoEntidade', entity_type=entidade_1)
        make('lupa.DadoEntidade', entity_type=entidade_2)

        queryset = DadoEntidade.objects.all()
        entidades = DadoEntidadeAdmin._get_entities(queryset)

        response = self.dadoadmin.change_to_detail(
            request,
            queryset
        )

        _validator.assert_called_once_with(request, entidades)
        self.assertIsNone(response)

    @mock.patch.object(DadoEntidade, 'copy_to_detail')
    def test_executor(self, _copier):
        dado_base_id = 0
        dado_1_id = 1
        dado_2_id = 2

        entidade = make(
            'lupa.Entidade',
            name=entidade_name
        )
        make(
            'lupa.DadoEntidade',
            id=dado_base_id,
            entity_type=entidade
        )
        make(
            'lupa.DadoEntidade',
            id=dado_1_id,
            entity_type=entidade
        )
        make(
            'lupa.DadoEntidade',
            id=dado_2_id,
            entity_type=entidade,
        )
        queryset = DadoEntidade.objects.filter(id__in=[dado_1_id, dado_2_id])

        request = mock.MagicMock()
        request.POST = {
            'dado_base': dado_base_id
        }

        self.dadoadmin._execute_change(request, queryset)

        for call in _copier.call_args_list:
            # Only one argument
            self.assertEqual(len(call[0]), 1)
            argument = call[0][0]
            # The argument is a DadoEntidade
            self.assertTrue(isinstance(argument, DadoEntidade))
            self.assertEquals(argument.id, dado_base_id)

    @mock.patch.object(DadoEntidadeAdmin, '_render_changer')
    @mock.patch.object(DadoEntidadeAdmin, '_valida_entidade_detailer')
    def test_render_access(self, _validator, _render):
        request = mock.MagicMock()
        _validator.return_value = True

        entidade = make('lupa.Entidade')
        make('lupa.DadoEntidade', entity_type=entidade)
        make('lupa.DadoEntidade', entity_type=entidade)

        queryset = DadoEntidade.objects.all()
        self.dadoadmin.change_to_detail(
            request,
            queryset
        )

        _render.assert_called_once_with(request, queryset)

    @mock.patch.object(DadoEntidadeAdmin, '_execute_change')
    @mock.patch.object(DadoEntidadeAdmin, '_valida_entidade_detailer')
    def test_execution_access(self, _validator, _executor):
        request = mock.MagicMock()
        request.POST = {'apply': True}
        _validator.return_value = True

        entidade = make('lupa.Entidade')
        make('lupa.DadoEntidade', entity_type=entidade)
        make('lupa.DadoEntidade', entity_type=entidade)

        queryset = DadoEntidade.objects.all()
        self.dadoadmin.change_to_detail(
            request,
            queryset
        )

        _executor.assert_called_once_with(request, queryset)
