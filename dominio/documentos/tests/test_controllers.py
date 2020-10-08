from datetime import datetime
from unittest import TestCase, mock

from django.http import HttpResponse
from freezegun import freeze_time

from dominio.documentos.controllers import (
    BaseDocumentoController,
    MinutaPrescricaoController,
    ProrrogacaoICController,
)
from dominio.documentos.dao import (
    DadosAssuntoDAO,
    DadosPromotorDAO,
    MinutaPrescricaoDAO,
    ProrrogacaoICDAO,
)


class TestBaseDocumentoController(TestCase):
    def setUp(self):
        self.orgao_id = "5678"
        self.docu_dk = "12345"
        self.cpf = "1234567890"

        class ChildController(BaseDocumentoController):
            @property
            def context(self):
                return {"context": 1}

        self.controller = ChildController(
            self.orgao_id,
            self.docu_dk,
            self.cpf,
        )

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

    @freeze_time("2020-1-1")
    def test_data_hoje(self):
        data_hoje = self.controller.data_hoje
        expected = "01 de janeiro de 2020"

        self.assertEqual(data_hoje, expected)


class TestMinutaPrescricaoController(TestCase):
    def setUp(self):
        self.orgao_id = "5678"
        self.docu_dk = "12345"
        self.cpf = "1234567890"

        self.matricula = "12345678"
        self.nome = "fulano de tal"
        self.controller = MinutaPrescricaoController(
            self.orgao_id,
            self.docu_dk,
            self.cpf,
        )

        # Dados DAO assunto
        self.nome_delito = "Delito"
        self.lei_delito = "Artigo 111"
        self.max_pena = 10
        self.multiplicador = 2

        self.matricula_promotor = "12345"
        self.nome_promotor = "Nome"

        self.expected_promotor_data = {
            "matricula_promotor": self.matricula_promotor,
            "nome_promotor": self.nome_promotor,
        }

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

        self.expected_assunto_data = [
            {
                "nome_delito": self.nome_delito,
                "lei_delito": self.lei_delito,
                "max_pena": self.max_pena,
                "multiplicador": self.multiplicador,
            }
        ]

        self.expected_data.update(self.formatted_dao_data)
        self.expected_data.update(self.expected_promotor_data)
        self.expected_data.update(
            {
                "nome_delito": self.nome_delito,
                "lei_delito": self.lei_delito,
                "max_pena": "10 anos",
            }
        )

        self.dao_get_patcher = mock.patch.object(
            MinutaPrescricaoDAO, "get"
        )
        self.mock_dao_get = self.dao_get_patcher.start()
        self.mock_dao_get.return_value = self.expected_dao_data

        self.assunto_dao_patcher = mock.patch.object(
            DadosAssuntoDAO, "get"
        )
        self.mock_assunto_dao_get = self.assunto_dao_patcher.start()
        self.mock_assunto_dao_get.return_value = self.expected_assunto_data

        self.promotor_dao_patcher = mock.patch.object(
            DadosPromotorDAO, "get"
        )
        self.mock_promotor_dao_get = self.promotor_dao_patcher.start()
        self.mock_promotor_dao_get.return_value = self.expected_promotor_data

    def tearDown(self):
        self.dao_get_patcher.stop()
        self.assunto_dao_patcher.stop()
        self.promotor_dao_patcher.stop()

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

    def test_corrige_comarca(self):
        comarca_rj = "RIO DE JANEIRO"
        comarca_qualquer = "QUALQUER"

        corrigida_rj = self.controller.corrige_comarca(comarca_rj)
        corrigida_qualquer = self.controller.corrige_comarca(comarca_qualquer)
        expected_rj = "CAPITAL"
        expected_qualquer = "QUALQUER"

        self.assertEqual(corrigida_rj, expected_rj)
        self.assertEqual(corrigida_qualquer, expected_qualquer)


class TestResponsavelMinuta(TestCase):
    def setUp(self):
        self.orgao_id = "5678"
        self.docu_dk = "12345"
        self.cpf = "1234567890"

        self.controller = MinutaPrescricaoController(
            self.orgao_id, self.docu_dk, self.cpf
        )

        self.dados_promotor_patcher = mock.patch.object(
            DadosPromotorDAO, "get"
        )

        self.nome_promotor = "Nome"
        self.matricula_promotor = "12345"

        self.expected_responsavel = {
            "nome_promotor": self.nome_promotor,
            "matricula_promotor": self.matricula_promotor
        }

        self.mock_dados_promotor = self.dados_promotor_patcher.start()
        self.mock_dados_promotor.return_value = self.expected_responsavel

    def tearDown(self):
        self.dados_promotor_patcher.stop()

    def test_get_reponsavel(self):
        responsavel = self.controller.responsavel

        self.assertEqual(responsavel, self.expected_responsavel)


class TestDelitosMinuta(TestCase):
    def setUp(self):
        self.orgao_id = "5678"
        self.docu_dk = "12345"
        self.cpf = "1234567890"

        self.controller = MinutaPrescricaoController(
            self.orgao_id, self.docu_dk, self.cpf
        )

        self.dados_assunto_patcher = mock.patch.object(
            DadosAssuntoDAO, "get"
        )

        self.nome_delito = ["Delito 1", "Delito 2"]
        self.lei_delito = ["Artigo 1", "Artigo 2"]
        self.max_pena = [5, 10]
        self.multiplicador = [1, 2]

        self.dao_delitos_data = [
            {
                "nome_delito": self.nome_delito[0],
                "lei_delito": self.lei_delito[0],
                "max_pena": self.max_pena[0],
                "multiplicador": self.multiplicador[0],
            },
            {
                "nome_delito": self.nome_delito[1],
                "lei_delito": self.lei_delito[1],
                "max_pena": self.max_pena[1],
                "multiplicador": self.multiplicador[1],
            },
        ]

        self.mock_dados_assunto = self.dados_assunto_patcher.start()
        self.mock_dados_assunto.return_value = self.dao_delitos_data

        self.expected_delitos = {
            "nome_delito": self.nome_delito[1],
            "lei_delito": self.lei_delito[1],
            "max_pena": "50 anos"
        }

    def tearDown(self):
        self.dados_assunto_patcher.stop()

    def test_get_delitos(self):
        delitos = self.controller.delitos

        self.assertEqual(delitos, self.expected_delitos)


class TestModeloProrrogacaoProcedimento(TestCase):
    def setUp(self):
        self.orgao_id = "5678"
        self.docu_dk = "12345"
        self.cpf = "1234567890"
        self.controller = ProrrogacaoICController(
            self.orgao_id,
            self.docu_dk,
            self.cpf,
        )

        self.num_procedimento = "12345"
        self.nome_promotor = "Nome"
        self.matricula_promotor = "012345"

        self.dao_docu_get_patcher = mock.patch.object(ProrrogacaoICDAO, "get")
        self.dao_docu_get_mock = self.dao_docu_get_patcher.start()
        self.dao_docu_get_mock.return_value = {
            "num_procedimento": self.num_procedimento,
        }

        self.dao_promotor_get_patcher = mock.patch.object(
            DadosPromotorDAO, "get"
        )
        self.dao_promotor_get_mock = self.dao_promotor_get_patcher.start()
        self.dao_promotor_get_mock.return_value = {
            "nome_promotor": self.nome_promotor,
            "matricula_promotor": self.matricula_promotor,
        }

        self.expected_context = {
            "num_procedimento": self.num_procedimento,
            "data_hoje": "01 de janeiro de 2020",
            "nome_promotor": self.nome_promotor,
            "matricula_promotor": self.matricula_promotor,
        }

    def tearDown(self):
        self.dao_docu_get_patcher.stop()
        self.dao_promotor_get_patcher.stop()

    @freeze_time("2020-1-1")
    def test_get_context(self):
        context = self.controller.context

        self.assertEqual(context, self.expected_context)
