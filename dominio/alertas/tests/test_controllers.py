from unittest import mock

from django.conf import settings
from django.test import TestCase

from dominio.alertas import controllers


class TestEnviaAlertaComprasOuvidoriaController(TestCase):
    def setUp(self):
        self.alerta_sigla = (
            controllers.EnviaAlertaComprasOuvidoriaController.alerta_sigla
        )
        self.orgao_id = "12345"
        self.alerta_id = "abc12345"

        self.controller = controllers.EnviaAlertaComprasOuvidoriaController(
            orgao_id=self.orgao_id,
            alerta_id=self.alerta_id
        )

        self.get_hbase_table_patcher = mock.patch(
            "dominio.alertas.controllers.get_hbase_table"
        )
        self.get_hbase_table_mock = self.get_hbase_table_patcher.start()
        self.hbase_table_mock = mock.Mock()
        self.hbase_table_mock.scan.return_value = iter('')
        self.get_hbase_table_mock.return_value = self.hbase_table_mock

    def tearDown(self):
        self.get_hbase_table_patcher.stop()

    def test_cria_chave_do_banco(self):
        expected = (
            f"alerta_ouvidoria_{self.orgao_id}_{self.alerta_sigla}"
            f"_{self.alerta_id}"
        )

        self.assertEqual(self.controller.get_row_key, expected)

    def test_envia_para_ouvidoria_com_sucesso(self):
        self.controller.envia()

        self.hbase_table_mock.scan.assert_called_once_with(
            row_prefix=self.controller.get_row_key
        )
        self.hbase_table_mock.put.assert_called_once_with(
            self.controller.get_row_key.encode(),
            self.controller.get_row_data  # TODO: test and create this method
        )

        connection_str = (
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            settings.HBASE_ALERTAS_OUVIDORIA_TABLE
        )
        self.assertEqual(
            self.get_hbase_table_mock.call_args_list,
            [mock.call(connection_str), mock.call(connection_str)]
        )
