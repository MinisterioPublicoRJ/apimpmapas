from django.core.management import call_command
from django.test import TestCase
from model_mommy.mommy import make
from unittest import mock
from unittest.mock import call
from lupa.management.commands.checkconsistency import (
    Command,
    parsecolumns
)
from lupa.models import ColunaDado


class TestCheckConsistency(TestCase):

    def setUp(self):
        dadosimples = mock.MagicMock()
        dadosimples.database = 'DB'
        dadosimples.schema = 'SCM'
        dadosimples.table = 'TBL'
        self.dadosimples = dadosimples
        self.columns = ['a', 'b']

    @mock.patch.object(Command, 'stdout.write')
    def simpleprinttest(self, _wrt):
        command = Command()
        command.printok("OKMSG", "OKEND")
        command.printok("NOKMSG", "NOKEND")
        command.printok("STATUSMSG", "STATUSEND")

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
            _wrt.call_args_list,
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
        side_effect=Exception("QUERY ERROR")
    )
    def test_process_data_error(self, _excs, _ptst, _ptnok):
        mdado = make(
            'lupa.Dado',
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

        command = Command()
        command.process_data(mdado)

        _ptst.assert_called_once_with(
            f'Dado: Bairro id=3 - ',
            end=' '
        )
        _ptnok.assert_called_once_with(
            'NOK - DB - SCHM - TBL', Exception('QUERY ERROR')
        )
        _excs.assert_called_once_with('a')
