from django.core.management import call_command
from django.test import TestCase
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
                ColunaDado(name='N%s' % i, info_type='I%s' % i),
                'N%s as I%s' % (i, i)
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
