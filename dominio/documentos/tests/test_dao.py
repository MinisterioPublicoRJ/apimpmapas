from datetime import datetime
from decimal import Decimal
from unittest import mock

from django.test import TestCase

from dominio.documentos.dao import DadosPromotorDAO, MinutaPrescricaoDAO


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
