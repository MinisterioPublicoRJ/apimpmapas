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

        self.expected_message = (
            f"<html>\n  <body>\n    {self.orgao_id} - {self.alerta_id}"
            "\n  </body>\n</html>\n"
        )
        self.expected_context = Context(
            {
                "orgao_id": self.orgao_id,
                "alerta_id": self.alerta_id,
            }
        )

    def test_get_message_context(self):
        context = self.messager.context

        self.assertEqual(context, self.expected_context)

    def test_render_message(self):
        msg = self.messager.render()

        self.assertEqual(msg, self.expected_message)
