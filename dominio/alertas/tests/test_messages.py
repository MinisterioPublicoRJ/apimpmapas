from unittest import mock

from django.template import Context
from django.test import TestCase


from dominio.alertas import messages


class TestMensagemAlertaComprasOuvidoria(TestCase):
    def setUp(self):
        self.orgao_id = "12345"
        self.alerta_id = "abc12345"
        self.messager = messages.MensagemOuvidoriaCompras(
            self.orgao_id,
            self.alerta_id
        )

        self.expected_message = "msg"
        self.expected_context = Context(
            {
                "orgao_id": self.orgao_id,
                "alerta_id": self.alerta_id,
            }
        )

        self.template_obj_mock = mock.Mock()
        self.template_obj_mock.render.return_value = self.expected_message
        self.template_patcher = mock.patch("dominio.alertas.messages.Template")
        self.template_mock = self.template_patcher.start()
        self.template_mock.return_value = self.template_obj_mock

    def tearDown(self):
        self.template_patcher.stop()

    def test_get_message_context(self):
        context = self.messager.context

        self.assertEqual(context, self.expected_context)

    def test_render_message(self):
        msg = self.messager.render()

        self.template_mock.assert_called()
        self.template_obj_mock.render.assert_called_once_with(
            context=self.messager.context
        )
        self.assertEqual(msg, self.expected_message)
