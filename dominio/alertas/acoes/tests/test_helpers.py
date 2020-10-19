from unittest import TestCase

from dominio.alertas.acoes.helpers import lista_procs_ausentes


class TestListaROsAusentes(TestCase):
    def setUp(self):
        self.lista_procs = [
            {"proc_numero_serial": 10},
            {"proc_numero_serial": 12},
            {"proc_numero_serial": 23},
            {"proc_numero_serial": 44},
        ]
        self.expected_proc_numeros = (
            list(range(10))
            + [11]
            + list(range(13, 23))
            + list(range(24, 44))
        )

    def test_cria_lista_de_ros_ausentes(self):
        numeros_ausentes = lista_procs_ausentes(self.lista_procs)

        self.assertEqual(numeros_ausentes, self.expected_proc_numeros)
