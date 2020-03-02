from unittest import mock, TestCase

from django.conf import settings

from dominio.suamesa import get_regras, QUERY_REGRAS


class TestSuaMesa(TestCase):
    @mock.patch('dominio.suamesa.run_query')
    def test_sua_mesa_get_regras_investigacao(self, _run_query):
        _run_query.return_value = [(20,), (30,)]

        orgao_id = 10
        output = get_regras(orgao_id, 'investigacao')
        expected_output = [20, 30]

        expected_query = QUERY_REGRAS.format(
            regras_table="tb_regra_negocio_investigacao",
            namespace=settings.TABLE_NAMESPACE
        )
        expected_parameters = {
            'orgao_id': orgao_id
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)
        self.assertEqual(output, expected_output)

    @mock.patch('dominio.suamesa.run_query')
    def test_sua_mesa_get_regras_processo(self, _run_query):
        _run_query.return_value = [(20,), (30,)]

        orgao_id = 10
        output = get_regras(orgao_id, 'processo')
        expected_output = [20, 30]

        expected_query = QUERY_REGRAS.format(
            regras_table="tb_regra_negocio_processo",
            namespace=settings.TABLE_NAMESPACE
        )
        expected_parameters = {
            'orgao_id': orgao_id
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)
        self.assertEqual(output, expected_output)
