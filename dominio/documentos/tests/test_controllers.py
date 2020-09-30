from datetime import datetime
from unittest import TestCase, mock

from django.http import HttpResponse
from freezegun import freeze_time

from dominio.documentos.controllers import MinutaPrescricaoController
from dominio.documentos.dao import DadosUsuarioDAO, MinutaPrescricaoDAO


class TestMinutaPrescricaoController(TestCase):
    def setUp(self):
        self.docu_dk = "12345"
        self.matricula = "12345678"
        self.nome = "fulano de tal"
        self.controller = MinutaPrescricaoController(
            self.docu_dk,
            self.matricula
        )
        self.expected_dao_data = {
            "data": "data",
            "data_fato": datetime.strptime('01/01/00', '%d/%m/%y'),
            "comarca_tj": "NITEROI",
        }
        self.expected_data = {
            "data_hoje": "01 de janeiro de 2020",
            "preposicao_comarca": "DE",
        }
        self.expected_data.update(self.expected_dao_data)

        self.formatted_dao_data = {
            "data_fato": "01 de janeiro de 2000",
        }
        self.expected_data.update(self.formatted_dao_data)

        self.expected_user_data = {
            "matricula": self.matricula,
            "nome": self.nome,
        }
        self.expected_data.update(self.expected_user_data)

        self.http_response = HttpResponse()

        self.mock_docx_patcher = mock.patch(
            "dominio.documentos.controllers.DocxTemplate"
        )
        self.mock_docx = self.mock_docx_patcher.start()
        self.mock_docx_template = mock.Mock()
        self.mock_docx.return_value = self.mock_docx_template

        self.dao_get_patcher = mock.patch.object(
            MinutaPrescricaoDAO, "get"
        )
        self.mock_dao_get = self.dao_get_patcher.start()
        self.mock_dao_get.return_value = self.expected_dao_data

        self.user_dao_patcher = mock.patch.object(
            DadosUsuarioDAO, "get"
        )
        self.mock_user_dao_get = self.user_dao_patcher.start()
        self.mock_user_dao_get.return_value = self.expected_user_data

    def tearDown(self):
        self.mock_docx_patcher.stop()
        self.dao_get_patcher.stop()
        self.user_dao_patcher.stop()

    def test_render_document(self):
        self.controller.render(self.http_response)

        self.mock_docx.assert_called_once_with(self.controller.template)
        self.mock_docx_template.render.assert_called_once_with(
            self.controller.context
        )
        self.mock_docx_template.save.assert_called_once_with(
            self.http_response
        )

    @freeze_time('2020-01-01')
    def test_get_context_data(self):
        context = self.controller.context

        self.assertEqual(context, self.expected_data)

    def test_get_preposicao_comarca(self):
        expected_preposicao = {
            "QUALQUER": "DE",
            "CAPITAL": "DA",
            "RIO DE JANEIRO": "DO",
        }

        for key, value in expected_preposicao.items():
            with self.subTest():
                self.assertEqual(value, self.controller.get_preposicao(key))
