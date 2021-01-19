from unittest import mock

from django.conf import settings
from django.test import TestCase

from dominio.alertas import controllers


class TestDispensaAlertasController(TestCase):
    def setUp(self):
        self.orgao_id = "12345"
        self.alerta_id = "AAA.abc12345.12345"
        self.alerta_sigla = "AAA"

        self.hbase_table_name = "table_name"
        self.hbase_cf = "cf"
        self.hbase_all_table_name = "table_name_todos"

        self.controller = controllers.DispensaAlertaController(
            self.orgao_id,
            self.alerta_id
        )
        self.controller.hbase_table_name = self.hbase_table_name
        self.controller.hbase_cf = self.hbase_cf
        self.controller.hbase_all_table_name = self.hbase_all_table_name
        self.controller.hbase_all_cf = self.hbase_cf

        self.get_hbase_table_patcher = mock.patch(
            "dominio.alertas.controllers.get_hbase_table"
        )
        self.get_hbase_table_mock = self.get_hbase_table_patcher.start()
        self.hbase_obj_mock = mock.Mock()
        self.get_hbase_table_mock.return_value = self.hbase_obj_mock

        self.expected_hbase_key = (
            f"{self.alerta_id}".encode()
        )
        self.expected_hbase_data = {
           f"{self.hbase_cf}:orgao".encode(): self.orgao_id.encode(),
           f"{self.hbase_cf}:sigla".encode(): self.alerta_sigla.encode(),
           f"{self.hbase_cf}:alerta_id".encode(): self.alerta_id.encode(),
        }

    def tearDown(self):
        self.get_hbase_table_patcher.stop()

    def test_dispensa_alerta_para_orgao(self):
        self.controller.dispensa_para_orgao()

        self.get_hbase_table_mock.assert_called_once_with(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            self.hbase_table_name
        )
        self.hbase_obj_mock.put.assert_called_once_with(
            self.expected_hbase_key,
            self.expected_hbase_data
        )

    def test_retorna_alerta_para_orgao(self):
        self.controller.retorna_para_orgao()

        self.get_hbase_table_mock.assert_called_once_with(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            self.hbase_table_name
        )
        self.hbase_obj_mock.delete.assert_called_once_with(
            self.expected_hbase_key,
        )

    def test_dispensa_alerta_para_todos_orgaos(self):
        self.expected_hbase_key = (
            f"{'.'.join(self.alerta_id.split('.')[:-1])}".encode()
        )
        self.expected_hbase_data[f"{self.hbase_cf}:orgao".encode()] = b"ALL"
        self.expected_hbase_data[f"{self.hbase_cf}:alerta_id".encode()] = self.expected_hbase_key

        self.controller.dispensa_para_todos_orgaos()

        self.get_hbase_table_mock.assert_called_once_with(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            self.hbase_all_table_name
        )
        self.hbase_obj_mock.put.assert_called_once_with(
            self.expected_hbase_key,
            self.expected_hbase_data
        )

    def test_retorna_alerta_para_todos_orgaos(self):
        self.expected_hbase_key = (
            f"{'.'.join(self.alerta_id.split('.')[:-1])}".encode()
        )

        self.controller.retorna_para_todos_orgaos()

        self.get_hbase_table_mock.assert_called_once_with(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            self.hbase_all_table_name
        )
        self.hbase_obj_mock.delete.assert_called_once_with(
            self.expected_hbase_key,
        )


class TestEnviaAlertaOuvidoriaController(TestCase):
    def setUp(self):
        self.orgao_id = "12345"
        self.alerta_id = "AAA.abc12345.12345"
        self.alerta_sigla = "AAA"

        self.hbase_table_name = "table_name"

        self.controller = controllers.EnviaAlertaOuvidoriaController(
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

        self.dispensa_cont_obj_mock = mock.Mock()
        self.dispensa_cont_mock = mock.Mock()
        self.dispensa_cont_mock.return_value = self.dispensa_cont_obj_mock

        self.expected_msg = "<html></html>"
        self.messager_obj_mock = mock.Mock()
        self.messager_obj_mock.render.return_value = self.expected_msg
        self.messager_mock = mock.Mock()
        self.messager_mock.return_value = self.messager_obj_mock

        self.controller.hbase_table_name = self.hbase_table_name
        self.controller.alerta_sigla = self.alerta_sigla
        self.controller.messager_class = self.messager_mock
        self.controller.dispensa_controller_class = self.dispensa_cont_mock

        self.expected_resp = {
            "detail": "Alerta enviado para ouvidoria com sucesso"
        }
        self.expected_status = 201
        self.expected_row_key = (
            f"{self.alerta_id}"
        ).encode()
        cf = self.controller.hbase_cf
        self.expected_data = {
            f"{cf}:orgao".encode(): self.orgao_id.encode(),
            f"{cf}:alerta_id".encode(): self.alerta_id.encode(),
            f"{cf}:sigla".encode(): self.controller.alerta_sigla.encode(),
        }

    def tearDown(self):
        self.get_hbase_table_patcher.stop()
        self.async_envia_email_patcher.stop()

    def test_cria_chave_do_banco(self):
        self.assertEqual(self.controller.row_key, self.expected_row_key)

    def test_cria_dados_para_hbase(self):
        data = self.controller.row_data

        self.assertEqual(data, self.expected_data)

    def test_envia_email(self):
        self.controller.envia_email()

        self.async_envia_email_mock.delay.assert_called_once_with(
            self.controller
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

    def test_rollback_em_caso_de_erro(self):
        self.controller.rollback()

        self.hbase_table_mock.delete.assert_called_once_with(
            self.expected_row_key
        )

    def test_envia_para_ouvidoria_com_sucesso(self):
        resp, status = self.controller.envia()

        self.hbase_table_mock.scan.assert_called_once_with(
            row_prefix=self.expected_row_key
        )
        self.hbase_table_mock.put.assert_called_once_with(
            self.expected_row_key,
            self.expected_data
        )

        connection_str = (
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            self.hbase_table_name
        )
        self.assertEqual(
            self.get_hbase_table_mock.call_args_list,
            [mock.call(connection_str), mock.call(connection_str)]
        )
        self.async_envia_email_mock.delay.assert_called_once_with(
            self.controller
        )
        self.assertEqual(resp, self.expected_resp)
        self.assertEqual(status, self.expected_status)

    def test_email_ja_enviado_para_ouvidoria(self):
        self.hbase_table_mock.scan.return_value = iter((True,))

        resp, status = self.controller.envia()

        self.hbase_table_mock.scan.assert_called_once_with(
            row_prefix=self.expected_row_key
        )
        self.hbase_table_mock.put.assert_not_called()
        self.async_envia_email_mock.delay.assert_not_called()

        self.assertEqual(
            resp,
            {"detail": "Este alerta já foi enviado para ouvidoria"}
        )
        self.assertEqual(
            status,
            409
        )

    def test_render_mensagem_para_ouvidoria(self):
        msg = self.controller.render_message()

        self.assertEqual(msg, self.expected_msg)

    def test_success_method(self):
        self.controller.success()

        self.dispensa_cont_obj_mock.dispensa_para_todos_orgaos.\
            assert_called_once()
