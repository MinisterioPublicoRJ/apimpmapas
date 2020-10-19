from unittest import TestCase

from freezegun import freeze_time

from dominio.alertas.acoes.helpers import (
    formata_ros_ausentes,
    lista_procs_ausentes,
    ros_ausentes,
)


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
            "012-00001/2020",
            "012-00010/2020",
            "012-00100/2020",
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
            "012-00001/2019",
            "012-00010/2019",
            "012-00100/2019",
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
            "012-00002/2020",
            "012-00004/2020",
            "012-00005/2020",
        ]

    def test_get_lista_ros_ausentes(self):
        ros = ros_ausentes(
            self.numeros_existentes,
            self.num_delegacia,
            self.ano
        )

        self.assertEqual(ros, self.expected_ros)
