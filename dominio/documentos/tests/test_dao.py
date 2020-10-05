from datetime import datetime
from decimal import Decimal
from unittest import mock

from django.test import TestCase

from dominio.documentos.dao import (
    DadosAssuntoDAO,
    DadosPromotorDAO,
    MinutaPrescricaoDAO,
)


class TestMinutaDAO(TestCase):
    @mock.patch("dominio.dao.impala_execute")
    def test_get_correct(self, _impala_execute):
        num_procedimento = "num_proc"
        data_fato = datetime(2020, 10, 10, 0, 0)
        org_resp = Decimal("1234")
        comarca = "nome_comarca"
        tempo_passado = 12345
        docu_dk = 1234
        _impala_execute.return_value = [
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


class TestDadosPromotorDAO(TestCase):
    @mock.patch("dominio.dao.impala_execute")
    def test_get_correct(self, _impala_execute):
        nome_promotor = "Nome"
        matricula_promotor = "Matricula"

        cpf = "1234567890"
        _impala_execute.return_value = [
            (
                matricula_promotor,
                nome_promotor,
            ),
        ]
        expected_value = {
            "matricula_promotor": matricula_promotor,
            "nome_promotor": nome_promotor,
        }

        data = DadosPromotorDAO.get(cpf=cpf)

        self.assertEqual(data, expected_value)


class TestDadosAssuntoDAO(TestCase):
    @mock.patch("dominio.dao.impala_execute")
    def test_get_correct(self, _impala_execute):
        docu_dk = "12345"

        nome_delito = ["DELITO 1", "DELITO 2"]
        artigo_lei = ["Artigo 1", "Artigo 2"]
        max_pena = [5, 10]
        multiplicador = [1, 2]

        _impala_execute.return_value = [
            (
                nome_delito[0],
                artigo_lei[0],
                max_pena[0],
                multiplicador[0]
            ),
            (
                nome_delito[1],
                artigo_lei[1],
                max_pena[1],
                multiplicador[1]
            ),
        ]
        expected_value = [
            {
                "nome_delito": nome_delito[0],
                "artigo_lei": artigo_lei[0],
                "max_pena": max_pena[0],
                "multiplicador": multiplicador[0],
            },
            {
                "nome_delito": nome_delito[1],
                "artigo_lei": artigo_lei[1],
                "max_pena": max_pena[1],
                "multiplicador": multiplicador[1],
            },
        ]

        data = DadosAssuntoDAO.get(docu_dk=docu_dk)

        self.assertEqual(data, expected_value)
