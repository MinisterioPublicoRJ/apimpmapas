from unittest import TestCase, mock

from django.http import HttpResponse

from dominio.documentos.controllers import MinutaPrescricaoController


class TestMinutaPrescricaoController(TestCase):
    def setUp(self):
        self.docu_dk = "12345"
        self.controller = MinutaPrescricaoController(self.docu_dk)

        self.http_response = HttpResponse()

        self.mock_docx_patcher = mock.patch(
            "dominio.documentos.controllers.DocxTemplate"
        )
        self.mock_docx = self.mock_docx_patcher.start()
        self.mock_docx_template = mock.Mock()
        self.mock_docx.return_value = self.mock_docx_template

    def tearDown(self):
        self.mock_docx_patcher.stop()

    def test_render_document(self):
        self.controller.render(self.http_response)

        self.mock_docx.assert_called_once_with(self.controller.template)
        self.mock_docx_template.render.assert_called_once_with(
            self.controller.context
        )
        self.mock_docx_template.save.assert_called_once_with(
            self.http_response
        )
