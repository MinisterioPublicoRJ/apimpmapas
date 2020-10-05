from unittest import TestCase

from dominio.documentos.helpers import formata_pena


class TestFormataPena(TestCase):
    def test_formata_data_da_pena(self):
        penas_info = [
            {"input": 1.02, "output": "1 ano e 1 mês"},
            {"input": 25.049999999999997, "output": "25 anos e 1 mês"},
            {"input": 16.7, "output": "16 anos e 9 meses"},
            {"input": 10.0, "output": "10 anos"},
        ]

        for info in penas_info:
            with self.subTest():
                resp = formata_pena(info["input"])
                self.assertEqual(resp, info["output"])
