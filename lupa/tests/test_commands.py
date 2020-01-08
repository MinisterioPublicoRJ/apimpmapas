from datetime import datetime as dt
from unittest import mock
from unittest.mock import call, MagicMock

from django.core.management import call_command
from django.test import TestCase
from model_mommy.mommy import make

from lupa.management.commands.checkconsistency import (
    Command,
    parsecolumns
)
from lupa.models import ColunaDado, Entidade, DadoEntidade, DadoDetalhe


class TestCheckConsistency(TestCase):

    def setUp(self):
        dadosimples = mock.MagicMock()
        dadosimples.database = 'DB'
        dadosimples.schema = 'SCM'
        dadosimples.table = 'TBL'
        self.dadosimples = dadosimples
        self.columns = ['a', 'b']

    def test_simpleprint(self):
        command = Command()
        command.stdout.write = MagicMock()
        command.printok("OKMSG", "OKEND")
        command.printnok("NOKMSG", None, "NOKEND")
        command.printstatus("STATUSMSG", "STATUSEND")

        expected = [
            call(
                command.style.SUCCESS("OKMSG"),
                ending="OKEND"
            ),
            call(
                command.style.ERROR("NOKMSG"),
                ending="NOKEND"
            ),
            call(
                "STATUSMSG",
                ending="STATUSEND"
            ),
        ]

        self.assertEqual(
            command.stdout.write.call_args_list,
            expected
        )

    def test_parse_columns(self):
        builder = [
            [
                ColunaDado(name=f'N{i}', info_type=f'I{i}'),
                f'N{i} as I{i}'
            ]
            for i in range(3)
        ]

        columns, expected = zip(*builder)

        result = parsecolumns(columns)
        self.assertEqual(tuple(result), expected)

    @mock.patch(
        'lupa.management.commands.checkconsistency.execute_sample',
        return_value=[
            (1234, 'lero'),
            (4567, 'lala')
        ]
    )
    @mock.patch.object(Command, 'printok')
    def test_process_execution_happypath(self, _ptok, _excs):
        command = Command()
        command.process_execution(
            self.dadosimples,
            self.columns
        )

        self.assertEqual(_ptok.call_count, 2)
        expected = [call('OK', end=''), call('')]
        self.assertEqual(_ptok.call_args_list, expected)
        _excs.assert_called_once_with(
            self.dadosimples.database,
            self.dadosimples.schema,
            self.dadosimples.table,
            self.columns
        )

    @mock.patch(
        'lupa.management.commands.checkconsistency.execute_sample',
        return_value=[]
    )
    @mock.patch.object(Command, 'printok')
    @mock.patch.object(Command, 'printnok')
    def test_process_empty_list(self, _ptnok, _ptok, _excs):
        command = Command()

        command.process_execution(
            self.dadosimples,
            self.columns
        )

        _ptok.assert_called_with('OK', end='')
        _ptnok.assert_called_with(' SEM RESULTADOS')

        _excs.assert_called_once_with(
            self.dadosimples.database,
            self.dadosimples.schema,
            self.dadosimples.table,
            self.columns
        )

    @mock.patch(
        'lupa.management.commands.checkconsistency.execute_sample',
        side_effect=Exception('QUERY ERROR')
    )
    def test_process_exception(self, _excs):
        command = Command()

        with self.assertRaisesMessage(Exception, 'QUERY ERROR'):
            command.process_execution(
                self.dadosimples,
                self.columns
            )

        _excs.assert_called_once_with(
            self.dadosimples.database,
            self.dadosimples.schema,
            self.dadosimples.table,
            self.columns
        )

    @mock.patch.object(Command, 'printnok')
    @mock.patch.object(Command, 'printstatus')
    @mock.patch(
        'lupa.management.commands.checkconsistency.execute_sample',
        return_value=[1, 2, 3]
    )
    def test_process_data_detail(self, _excs, _ptst, _ptnok):
        dado = make(
            'lupa.DadoEntidade',
        )
        make(
            'lupa.DadoDetalhe',
            dado_main=dado
        )
        make(
            'lupa.DadoDetalhe',
            dado_main=dado
        )

        dets = dado.data_details.all().order_by('id').all()

        command = Command()
        command.process_data(dado)

        self.assertEqual(
            len(_excs.call_args_list),
            3
        )
        self.assertEqual(
            len(_ptst.call_args_list),
            3
        )
        self.assertEqual(
            len(_ptnok.call_args_list),
            0
        )

        calls = [
            call(
                dado.database,
                dado.schema,
                dado.table,
                []
            )
        ]

        calls.extend(
            [
                call(
                    det.database,
                    det.schema,
                    det.table,
                    []
                ) for det in dets
            ]
        )

        self.assertEqual(
            _excs.call_args_list,
            calls
        )

    @mock.patch.object(Command, 'printnok')
    @mock.patch.object(Command, 'printstatus')
    def test_process_data_error(self, _ptst, _ptnok):
        mdado = make(
            'lupa.DadoEntidade',
            title='Bairro',
            id=3,
            database='DB',
            schema='SCHM',
            table='TBL'
        )

        make('lupa.ColunaDado', dado=mdado, name='A', info_type='CA'),
        make('lupa.ColunaDado', dado=mdado, name='B', info_type='CB')
        make('lupa.ColunaDado', dado=mdado, name='C', info_type='CC')
        make('lupa.ColunaDado', dado=mdado, name='D', info_type='CD')
        make('lupa.ColunaDado', dado=mdado, name='E', info_type='CE')

        error = Exception("QUERY ERROR")
        command = Command()
        with mock.patch(
            'lupa.management.commands.checkconsistency.execute_sample',
            side_effect=error
        ) as _excs:
            command.process_data(mdado)
            _excs.assert_called_once_with(
                'DB',
                'SCHM',
                'TBL',
                [
                    'E as CE',
                    'D as CD',
                    'C as CC',
                    'B as CB',
                    'A as CA'
                ]
            )

        _ptst.assert_called_once_with(
            f'Dado: Bairro id=3 - ',
            end=' '
        )

        _ptnok.assert_called_once_with(
            'NOK - DB - SCHM - TBL', error
        )

    @mock.patch.object(Command, 'printnok')
    @mock.patch.object(Command, 'printstatus')
    @mock.patch(
        'lupa.management.commands.checkconsistency.execute_sample',
        return_value=[
            ('a', 'b'),
            ('c', 'd')
        ]
    )
    def test_process_data(self, _excs, _ptst, _prok):
        command = Command()
        mdado = make(
            'lupa.DadoEntidade',
            title='Bairro',
            id=3,
            database='DB',
            schema='SCHM',
            table='TBL'
        )

        make('lupa.ColunaDado', dado=mdado, name='A', info_type='CA'),
        make('lupa.ColunaDado', dado=mdado, name='B', info_type='CB')
        make('lupa.ColunaDado', dado=mdado, name='C', info_type='CC')
        make('lupa.ColunaDado', dado=mdado, name='D', info_type='CD')
        make('lupa.ColunaDado', dado=mdado, name='E', info_type='CE')
        command.process_data(mdado)
        _excs.assert_called_once_with(
            'DB',
            'SCHM',
            'TBL',
            [
                'E as CE',
                'D as CD',
                'C as CC',
                'B as CB',
                'A as CA'
            ]
        )

        _ptst.assert_called_once_with('Dado: Bairro id=3 - ', end=' ')

    @mock.patch.object(Command, 'process_data')
    @mock.patch.object(Command, 'printstatus')
    def test_handle_happy_path(self, _prtst, _prd):
        mentidade = make(
            'lupa.Entidade',
            id=4,
            name="Entidade Teste"
        )
        mdado = make(
            'lupa.DadoEntidade',
            title='Bairro',
            id=3,
            database='DB',
            schema='SCHM',
            table='TBL',
            entity_type=mentidade
        )

        call_command('checkconsistency', 4)
        _prd.assert_called_with(mdado)
        _prtst.assert_called_once_with(
            "Verificando Dado(caixinhas) para entidade Entidade Teste"
        )


class UpdateCache(TestCase):
    @mock.patch(
        'lupa.management.commands.update_cache._repopulate_cache_data_entity'
    )
    def test_update_data_entidade_cache(self, _repopulate_cache_entity):
        key_prefix = 'lupa_dado_entidade'
        make(
            'lupa.DadoEntidade',
            cache_timeout_days=7,
            last_cache_update=dt(2019, 10, 15, 12, 0, 0),
        )
        make(
            'lupa.DadoEntidade',
            cache_timeout_days=7,
            last_cache_update=dt(2019, 10, 14, 12, 0, 0),
        )

        call_command('update_cache', 'dado_entidade')

        expiring_data = DadoEntidade.cache.expiring()
        args_prefix, args_queryset\
            = _repopulate_cache_entity.call_args_list[0][0]

        self.assertEqual(args_prefix, key_prefix)
        self.assertCountEqual(expiring_data, args_queryset)

    @mock.patch(
        'lupa.management.commands.update_cache._repopulate_cache_data_detail'
    )
    def test_update_data_detalhe_cache(self, _repopulate_cache_detail):
        key_prefix = 'lupa_dado_detalhe'
        make(
            'lupa.DadoDetalhe',
            cache_timeout_days=7,
            last_cache_update=dt(2019, 10, 15, 12, 0, 0),
        )
        make(
            'lupa.DadoDetalhe',
            cache_timeout_days=7,
            last_cache_update=dt(2019, 10, 14, 12, 0, 0),
        )

        call_command('update_cache', 'dado_detalhe')

        expiring_data = DadoDetalhe.cache.expiring()
        args_prefix, args_queryset\
            = _repopulate_cache_detail.call_args_list[0][0]

        self.assertEqual(args_prefix, key_prefix)
        self.assertCountEqual(expiring_data, args_queryset)

    @mock.patch(
        'lupa.management.commands.update_cache._repopulate_cache_entity'
    )
    def test_update_entity_cache(self, _repopulate_cache_entity):
        key_prefix = 'lupa_entidade'

        make(
            'lupa.Entidade',
            _quantity=2,
            last_cache_update=dt(2019, 10, 10)
        )

        call_command('update_cache', 'entidade')

        expiring_entity = Entidade.cache.expiring()
        args_prefix, args_queryset\
            = _repopulate_cache_entity.call_args_list[0][0]

        self.assertEqual(args_prefix, key_prefix)
        self.assertCountEqual(expiring_entity, args_queryset)

    def test_update_cache_object_doesnt_exist(self):
        with self.assertRaises(ValueError):
            call_command('update_cache', 'doesn_exist')
