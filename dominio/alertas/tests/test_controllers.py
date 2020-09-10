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

        self.async_envia_email_patcher = mock.patch(
            "dominio.alertas.controllers.async_envia_email_ouvidoria"
        )
        self.async_envia_email_mock = self.async_envia_email_patcher.start()

        self.expected_resp = {
            "detail": "Alerta enviado para ouvidoria com sucesso"
        }
        self.expected_status = 201

    def tearDown(self):
        self.get_hbase_table_patcher.stop()
        self.async_envia_email_patcher.stop()

    def test_cria_chave_do_banco(self):
        expected = (
            f"alerta_ouvidoria_{self.orgao_id}_{self.alerta_sigla}"
            f"_{self.alerta_id}"
        ).encode()

        self.assertEqual(self.controller.get_row_key, expected)

    def test_cria_dados_para_hbase(self):
        data = self.controller.get_row_data
        cf = self.controller.hbase_cf
        expected_data = {
            f"{cf}:orgao".encode(): self.orgao_id.encode(),
            f"{cf}:alerta_id".encode(): self.alerta_id.encode(),
            f"{cf}:sigla".encode(): self.controller.alerta_sigla.encode(),
        }

        self.assertEqual(data, expected_data)

    def test_envia_email(self):
        self.controller.envia_email()

        self.async_envia_email_mock.delay.assert_called_once_with(
            self.controller.orgao_id,
            self.controller.alerta_sigla,
            self.controller.alerta_id,
        )

    def test_prepara_resposta_email_ainda_nao_enviado(self):
        already_sent = False
        resp, status = self.controller.prepara_resposta(already_sent)

        self.assertEqual(
            resp,
            {"detail": "Alerta enviado para ouvidoria com sucesso"}
        )
        self.assertEqual(status, 201)

    def test_prepara_resposta_email_ja_enviado(self):
        already_sent = True
        resp, status = self.controller.prepara_resposta(already_sent)

        self.assertEqual(
            resp,
            {"detail": "Este alerta já foi enviado para ouvidoria"}
        )
        self.assertEqual(status, 409)

    def test_envia_para_ouvidoria_com_sucesso(self):
        resp, status = self.controller.envia()

        self.hbase_table_mock.scan.assert_called_once_with(
            row_prefix=self.controller.get_row_key
        )
        self.hbase_table_mock.put.assert_called_once_with(
            self.controller.get_row_key,
            self.controller.get_row_data
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
        self.async_envia_email_mock.delay.assert_called_once_with(
            self.controller.orgao_id,
            self.controller.alerta_sigla,
            self.controller.alerta_id,
        )
        self.assertEqual(resp, self.expected_resp)
        self.assertEqual(status, self.expected_status)
