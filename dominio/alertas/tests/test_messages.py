from unittest import mock

from django.template import Context
from django.test import TestCase, override_settings


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
        self.contratacao = 123
        self.dao_alerta_get_mock = self.dao_alerta_get_patcher.start()
        self.dao_data = {"contratacao": self.contratacao}
        self.dao_alerta_get_mock.return_value = self.dao_data

        self.expected_link_painel = (
            f"url.com?VAL={self.alerta_id}&CONT={self.contratacao}"
        )

        self.expected_context = {
            **self.dao_data, **{"link_painel": self.expected_link_painel}
        }

    def tearDown(self):
        self.template_patcher.stop()
        self.dao_alerta_get_patcher.stop()

    @override_settings(
        URL_PAINEL_COMPRAS="url.com?VAL={contrato_iditem}&CONT={contratacao}"
    )
    def test_get_message_context(self):
        context = self.messager.context

        self.assertEqual(context, self.expected_context)
        self.dao_alerta_get_mock.asseert_called_once_with(self.alerta_id)

    @override_settings(
        URL_PAINEL_COMPRAS="url.com?VAL={contrato_iditem}&CONT={contratacao}"
    )
    def test_get_link_painel(self):
        link_painel = self.messager.get_link_painel(self.contratacao)

        self.assertEqual(link_painel, self.expected_link_painel)

    def test_render_message(self):
        msg = self.messager.render()

        self.template_mock.assert_called()
        self.template_obj_mock.render.assert_called_once_with(
            context=Context(self.messager.context)
        )
        self.assertEqual(msg, self.expected_message)
