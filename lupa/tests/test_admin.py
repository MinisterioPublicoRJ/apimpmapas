from django.contrib.admin.sites import AdminSite
from model_mommy.mommy import make
from unittest import TestCase, mock
from lupa.admin import DadoEntidadeAdmin
from lupa.models import DadoEntidade
import pytest


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
