from unittest import mock

from django.template import Context
from django.test import TestCase


from dominio.alertas import dao
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

        self.template_obj_mock = mock.Mock()
        self.template_obj_mock.render.return_value = self.expected_message
        self.template_patcher = mock.patch("dominio.alertas.messages.Template")
        self.template_mock = self.template_patcher.start()
        self.template_mock.return_value = self.template_obj_mock

        self.dao_alerta_get_patcher = mock.patch.object(
            dao.DetalheAlertaCompraDAO, "get"
        )
        self.dao_alerta_get_mock = self.dao_alerta_get_patcher.start()
        self.context_data = {"data": 1}
        self.dao_alerta_get_mock.return_value = self.context_data
        self.expected_context = Context(
            self.context_data
        )

    def tearDown(self):
        self.template_patcher.stop()
        self.dao_alerta_get_patcher.stop()

    def test_get_message_context(self):
        context = self.messager.context

        self.assertEqual(context, self.expected_context)
        self.dao_alerta_get_mock.asseert_called_once_with(self.alerta_id)

    def test_render_message(self):
        msg = self.messager.render()

        self.template_mock.assert_called()
        self.template_obj_mock.render.assert_called_once_with(
            context=self.messager.context
        )
        self.assertEqual(msg, self.expected_message)
