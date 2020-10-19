from unittest import mock

from django.test import TestCase

from dominio.alertas.acoes import dao


class TestROsAusentes(TestCase):
    def setUp(self):
        self.num_delegacia = "12345"
        self.query_exec_patcher = mock.patch.object(
            dao.ListaROsAusentesDAO, "execute"
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
        data = dao.ListaROsAusentesDAO.get(num_delegacia=self.num_delegacia)

        self.assertEqual(data, self.expected_data)
