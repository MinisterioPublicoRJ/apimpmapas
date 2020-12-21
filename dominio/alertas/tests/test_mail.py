from unittest import mock

from django.conf import settings
from django.test import TestCase

from dominio.alertas.mail import envia_email_ouvidoria, email_login


class TestEmailLogin(TestCase):
    def setUp(self):
        self.smtp_patcher = mock.patch("dominio.alertas.mail.smtplib.SMTP")
        self.smtp_mock = self.smtp_patcher.start()

    def tearDown(self):
        self.smtp_patcher.stop()

    def test_loign(self):
        email_login()

        self.smtp_mock.assert_called_once_with(settings.EMAIL_SMTP_SERVER)


class TestEnviaEmailOuvidoria(TestCase):
    def setUp(self):
        self.email_login_patcher = mock.patch(
            "dominio.alertas.mail.email_login"
        )
        self.mime_patcher = mock.patch("dominio.alertas.mail.MIMEMultipart")

        self.server_mock = mock.Mock()
        self.email_login_mock = self.email_login_patcher.start()
        self.email_login_mock.return_value = self.server_mock

        self.mime_string = "mime string"
        self.subject = "subject"

        class CustomDict(dict):
            def as_string(self):
                return self.mime_string

            def set_charset(self):
                pass

            def attach(self):
                pass

        self.mime_multpart_mock = mock.MagicMock(spec=CustomDict)
        self.mime_multpart_mock.as_string.return_value = self.mime_string
        self.mime_mock = self.mime_patcher.start()
        self.mime_mock.return_value = self.mime_multpart_mock

        self.message = "<html><body>message</body></html>"

    def tearDown(self):
        self.email_login_patcher.stop()
        self.mime_patcher.stop()

    def test_envia_mensagem_por_email(self):
        envia_email_ouvidoria(self.message, self.subject)
        expected_from = settings.EMAIL_HOST_USER
        expected_dest = [settings.EMAIL_OUVIDORIA, settings.EMAIL_HOST_USER]

        self.email_login_mock.assert_called_once_with()
        self.server_mock.sendmail.assert_called_once_with(
            expected_from,
            expected_dest,
            self.mime_string,
        )
