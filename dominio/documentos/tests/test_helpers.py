from unittest import TestCase

import openpyxl
from freezegun import freeze_time

from dominio.documentos.helpers import (
    formata_lista,
    formata_pena,
    formata_ros_ausentes,
    gera_planilha_excel,
    lista_procs_ausentes,
    ros_ausentes,
    traduz_mes,
)


class TestFormataPena(TestCase):
    def test_formata_data_da_pena(self):
        penas_info = [
            {"input": 1.02, "output": "1 ano e 1 mês"},
            {"input": 25.049999999999997, "output": "25 anos e 1 mês"},
            {"input": 16.7, "output": "16 anos e 9 meses"},
            {"input": 10.0, "output": "10 anos"},
            {"input": 0.5, "output": "6 meses"},
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


class TestTraduzNomeMes(TestCase):
    def test_traduz_nome_mes(self):
        meses_info = [
            {"input": "1 January 1970", "output": "1 janeiro 1970"},
            {"input": "February", "output": "fevereiro"},
            {"input": "September", "output": "setembro"},
            {"input": "December", "output": "dezembro"},
        ]

        for info in meses_info:
            with self.subTest():
                resp = traduz_mes(info["input"])
                self.assertEqual(resp, info["output"])


class TestListaNumeroROsAusentes(TestCase):
    def setUp(self):
        self.lista_procs = [
            {"proc_numero_serial": 10},
            {"proc_numero_serial": 12},
            {"proc_numero_serial": 23},
            {"proc_numero_serial": 44},
        ]
        self.expected_proc_numeros = (
            list(range(1, 10))
            + [11]
            + list(range(13, 23))
            + list(range(24, 44))
        )

    def test_cria_lista_de_ros_ausentes(self):
        numeros_ausentes = lista_procs_ausentes(self.lista_procs)

        self.assertEqual(numeros_ausentes, self.expected_proc_numeros)


class TestFormataListaROs(TestCase):
    def setUp(self):
        self.numeros_ausentes = [1, 10, 100]
        self.num_delegacia = 12
        self.ano = 2020

        self.expected_ros = [
            (1, "012-00001/2020"),
            (2, "012-00010/2020"),
            (3, "012-00100/2020"),
        ]

    def test_formata_numeros_ros_ausentes(self):
        ros_formatados = formata_ros_ausentes(
            self.numeros_ausentes,
            self.num_delegacia,
            self.ano
        )

        self.assertEqual(ros_formatados, self.expected_ros)

    @freeze_time("2019-01-01")
    def test_utiliza_ano_corrente(self):
        self.expected_ros = [
            (1, "012-00001/2019"),
            (2, "012-00010/2019"),
            (3, "012-00100/2019"),
        ]
        ros_formatados = formata_ros_ausentes(
            self.numeros_ausentes,
            self.num_delegacia
        )
        self.assertEqual(ros_formatados, self.expected_ros)


class TestListaROsAusentes(TestCase):
    def setUp(self):
        self.num_delegacia = 12
        self.numeros_existentes = [
            {"proc_numero_serial": 1},
            {"proc_numero_serial": 3},
            {"proc_numero_serial": 6},
        ]
        self.ano = 2020

        self.expected_ros = [
            (1, "012-00002/2020"),
            (2, "012-00004/2020"),
            (3, "012-00005/2020"),
        ]

    def test_get_lista_ros_ausentes(self):
        ros = ros_ausentes(
            self.numeros_existentes,
            self.num_delegacia,
            self.ano
        )

        self.assertEqual(ros, self.expected_ros)


class TestCriaArquivoCSVROsAusentes(TestCase):
    def setUp(self):
        self.ros = [
            (1, "012-00002/2020"),
            (2, "012-00004/2020"),
            (3, "012-00005/2020"),
        ]
        self.header = ["id", "Número Procedimento"]
        self.sheet_title = "ROs ausentes"
        self.expected_data = [
            self.header,
            [1, "012-00002/2020"],
            [2, "012-00004/2020"],
            [3, "012-00005/2020"],
        ]

    def open_excel_file(self, file_obj):
        xlsx_file = openpyxl.load_workbook(file_obj)
        sheet = xlsx_file[xlsx_file.sheetnames[0]]
        rows = []
        for row in sheet.rows:
            rows.append([row[0].value, row[1].value])

        return rows

    def test_gera_arquivo_excel(self):
        excel_obj = gera_planilha_excel(
            self.ros,
            self.header,
            self.sheet_title
        )

        excel_data = self.open_excel_file(excel_obj)

        self.assertEqual(excel_data, self.expected_data)
