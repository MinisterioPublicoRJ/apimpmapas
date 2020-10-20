from datetime import datetime
from decimal import Decimal
from unittest import mock

from django.test import TestCase

from dominio.documentos.dao import (
    DadosAssuntoDAO,
    DadosPromotorDAO,
    InstauracaoICDAO,
    ListaROsAusentesDAO,
    MinutaPrescricaoDAO,
    ProrrogacaoICDAO,
    ProrrogacaoPPDAO,
)


class TestImpalaExecuteMixin:
    def setUp(self):
        self.patcher = mock.patch("dominio.dao.impala_execute")
        self._impala_execute = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()


class TestMinutaDAO(TestImpalaExecuteMixin, TestCase):
    def test_get_correct(self):
        num_procedimento = "num_proc"
        data_fato = datetime(2020, 10, 10, 0, 0)
        org_resp = Decimal("1234")
        comarca = "nome_comarca"
        tempo_passado = 12345
        docu_dk = 1234
        self._impala_execute.return_value = [
            (
                num_procedimento,
                data_fato,
                org_resp,
                comarca,
                tempo_passado,
            ),
        ]
        expected_value = {
            "num_procedimento": num_procedimento,
            "data_fato": data_fato,
            "orgao_responsavel": org_resp,
            "comarca_tj": comarca,
            "tempo_passado": tempo_passado,
        }

        data = MinutaPrescricaoDAO.get(docu_dk=docu_dk)

        self.assertEqual(data, expected_value)


class TestDadosPromotorDAO(TestImpalaExecuteMixin, TestCase):
    def test_get_correct(self):
        nome_promotor = "Nome"
        matricula_promotor = "00001234"
        sexo = "X"

        cpf = "00000000"
        self._impala_execute.return_value = [
            (
                matricula_promotor,
                nome_promotor,
                sexo,
            ),
        ]

        data = DadosPromotorDAO.get(cpf=cpf)
        expected_value = {
            "matricula_promotor": "1234",
            "nome_promotor": nome_promotor,
            "sexo": sexo
        }

        self.assertEqual(data, expected_value)


class TestDadosAssuntoDAO(TestImpalaExecuteMixin, TestCase):
    def test_get_correct(self):
        docu_dk = "00000"

        nome_delito = ["DELITO 1", "DELITO 2"]
        lei_delito = ["Artigo 1", "Artigo 2"]
        max_pena = [5, 10]
        multiplicador = [1, 2]

        self._impala_execute.return_value = [
            (
                nome_delito[0],
                lei_delito[0],
                max_pena[0],
                multiplicador[0]
            ),
            (
                nome_delito[1],
                lei_delito[1],
                max_pena[1],
                multiplicador[1]
            ),
        ]
        expected_value = [
            {
                "nome_delito": nome_delito[0],
                "lei_delito": lei_delito[0],
                "max_pena": max_pena[0],
                "multiplicador": multiplicador[0],
            },
            {
                "nome_delito": nome_delito[1],
                "lei_delito": lei_delito[1],
                "max_pena": max_pena[1],
                "multiplicador": multiplicador[1],
            },
        ]

        data = DadosAssuntoDAO.get(docu_dk=docu_dk)

        self.assertEqual(data, expected_value)


class TestProrrogacaoICDAO(TestImpalaExecuteMixin, TestCase):
    def test_get_prorrogacao_data(self):
        docu_dk = "1234"
        num_procedimento = "1111.2222.3333"
        comarca = "COMARCA"
        self._impala_execute.return_value = ((num_procedimento, comarca),)

        data = ProrrogacaoICDAO.get(docu_dk=docu_dk)
        expected = {
            "num_procedimento": num_procedimento,
            "comarca": comarca,
        }

        self.assertEqual(data, expected)


class TestProrrogacaoPPDAO(TestImpalaExecuteMixin, TestCase):
    def test_get_prorrogacao_data(self):
        docu_dk = "1234"
        num_procedimento = "1111.2222.3333"
        comarca = "COMARCA"
        self._impala_execute.return_value = ((num_procedimento, comarca),)

        data = ProrrogacaoPPDAO.get(docu_dk=docu_dk)
        expected = {
            "num_procedimento": num_procedimento,
            "comarca": comarca,
        }

        self.assertEqual(data, expected)


class TestInstauracaoICDAO(TestImpalaExecuteMixin, TestCase):
    def test_get_instauracao_data(self):
        docu_dk = "1234"
        num_procedimento = "1111.2222.3333"
        nome_promotoria = "PROMOTORIA"
        comarca = "COMARCA"
        objeto = "objeto"
        codigo_assunto = 12345
        atribuicao = "ATRIBUICAO"
        ementa = "EMENTA"
        investigados = "INVESTIGADOS"
        self._impala_execute.return_value = (
            (
                num_procedimento,
                nome_promotoria,
                comarca,
                objeto,
                codigo_assunto,
                atribuicao,
                ementa,
                investigados,
            ),
        )

        data = InstauracaoICDAO.get(docu_dk=docu_dk)
        expected = {
            "num_procedimento": num_procedimento,
            "nome_promotoria": nome_promotoria,
            "comarca": comarca,
            "objeto": objeto,
            "codigo_assunto": codigo_assunto,
            "atribuicao": atribuicao,
            "ementa": ementa,
            "investigados": investigados,
        }

        self.assertEqual(data, expected)


class TestROsAusentes(TestCase):
    def setUp(self):
        self.num_delegacia = "12345"
        self.query_exec_patcher = mock.patch.object(
            ListaROsAusentesDAO, "execute"
        )
        self.query_exec_mock = self.query_exec_patcher.start()
        self.result_set = (
            (1,),
            (2,),
            (3,),
        )
        self.query_exec_mock.return_value = self.result_set
        self.expected_data = [
            {"proc_numero_serial": 1},
            {"proc_numero_serial": 2},
            {"proc_numero_serial": 3},
        ]

    def tearDown(self):
        self.query_exec_patcher.stop()

    def test_get_data(self):
        data = ListaROsAusentesDAO.get(num_delegacia=self.num_delegacia)

        self.assertEqual(data, self.expected_data)
