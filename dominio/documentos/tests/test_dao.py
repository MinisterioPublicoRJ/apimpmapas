from datetime import datetime
from decimal import Decimal
from unittest import mock

from django.test import TestCase

from dominio.documentos.dao import (
    DadosAssuntoDAO,
    DadosPromotorDAO,
    MinutaPrescricaoDAO,
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
