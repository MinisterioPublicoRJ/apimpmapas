from unittest import TestCase

from dominio.documentos.helpers import formata_lista, formata_pena


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


class TestFormataListaComVirgula(TestCase):
    def test_formata_lista_um_elemento(self):
        lista = ["Info"]

        lista_formatada = formata_lista(lista)
        expected_lista = "Info"

        self.assertEqual(lista_formatada, expected_lista)

    def test_formata_lista_dois_elementos(self):
        lista = ["Info 1", "Info 2"]

        lista_formatada = formata_lista(lista)
        expected_lista = "Info 1 e Info 2"

        self.assertEqual(lista_formatada, expected_lista)

    def test_formata_lista_maior_que_dois_elementos(self):
        lista = ["Info 1", "Info 2", "Info 3"]

        lista_formatada = formata_lista(lista)
        expected_lista = "Info 1, Info 2 e Info 3"

        self.assertEqual(lista_formatada, expected_lista)
