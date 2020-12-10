from unittest import mock

from django.test import TestCase

from dominio.alertas import controllers
from dominio.alertas.tasks import async_envia_email_ouvidoria


class TestEnviaEmailOuvidoria(TestCase):
    def setUp(self):
        self.orgao_id = "12345"
        self.alerta_id = "abc12345"
        self.controller = controllers.EnviaAlertaComprasOuvidoriaController(
            self.orgao_id,
            self.alerta_id
        )

        self.mail_patcher = mock.patch(
            "dominio.alertas.tasks.envia_email_ouvidoria"
        )
        self.mail_mock = self.mail_patcher.start()

        self.messager_patcher = mock.patch.object(
            self.controller,
            "render_message"
        )
        self.expected_msg = "<html></html>"
        self.message_mock = self.messager_patcher.start()
        self.message_mock.return_value = self.expected_msg

    def tearDown(self):
        self.mail_patcher.stop()
        self.message_mock = self.messager_patcher.stop()

    def test_envia_email(self):
        async_envia_email_ouvidoria.run(self.controller)
        self.mail_mock.assert_called_once_with(
            self.expected_msg,
            self.controller.email_subject
        )

    @mock.patch.object(async_envia_email_ouvidoria, "retry")
    def test_envia_email_erro(self, _retry):
        self.mail_mock.side_effect = Exception

        async_envia_email_ouvidoria.run(self.controller)

        self.mail_mock.assert_called_once_with(
            self.expected_msg,
            self.controller.email_subject
        )
        _retry.assert_called()
