from unittest import mock

from django.test import TestCase

from dominio.alertas.tasks import async_envia_email_ouvidoria


class TestEnviaEmailOuvidoria(TestCase):
    def setUp(self):
        self.orgao_id = "12345"
        self.alerta_sigla = "COMP"
        self.alerta_id = "abc12345"

        self.mail_patcher = mock.patch(
            "dominio.alertas.tasks.envia_email_ouvidoria"
        )
        self.mail_mock = self.mail_patcher.start()

    def tearDown(self):
        self.mail_patcher.stop()

    def test_envia_email(self):
        async_envia_email_ouvidoria.run(
            self.orgao_id,
            self.alerta_sigla,
            self.alerta_id
        )

        self.mail_mock.assert_called_once_with("message")

    @mock.patch.object(async_envia_email_ouvidoria, "retry")
    def test_envia_email_erro(self, _retry):
        self.mail_mock.side_effect = Exception

        async_envia_email_ouvidoria.run(
            self.orgao_id,
            self.alerta_sigla,
            self.alerta_id
        )

        self.mail_mock.assert_called_once_with("message")
        _retry.assert_called()
