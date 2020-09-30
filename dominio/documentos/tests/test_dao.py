import os
from datetime import datetime
from decimal import Decimal
from unittest import mock

from django.test import TestCase

from dominio.documentos.dao import MinutaPrescricaoDAO


class TestMinutaDAO(TestCase):
    @mock.patch("dominio.dao.impala_execute")
    def test_get_correct(self, _impala_execute):
        num_procedimento = "num_proc"
        data_fato = datetime(2020, 10, 10, 0, 0)
        org_resp = Decimal("1234")
        comarca = "nome_comarca"
        tempo_passado = 12345
        assuntos = "assuntos, "
        leis = "leis, "
        docu_dk = 1234
        _impala_execute.return_value = [
            (
                num_procedimento,
                data_fato,
                org_resp,
                comarca,
                tempo_passado,
                assuntos,
                leis
            ),
        ]
        expected_value = {
            "num_procedimento": num_procedimento,
            "data_fato": data_fato,
            "orgao_responsavel": org_resp,
            "comarca_tj": comarca,
            "tempo_passado": tempo_passado,
            "assunto_docto": assuntos,
            "lei_docto": leis,
        }

        data = MinutaPrescricaoDAO.get(docu_dk=docu_dk)

        self.assertEqual(data, expected_value)
