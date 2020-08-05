from unittest import mock

from django.test import TestCase

from dominio.alertas import dao


class ResumoAlertasComprasDAOTest(TestCase):
    @mock.patch.object(dao.ResumoAlertasComprasDAO, "execute")
    def test_get_data(self, _execute):
        id_orgao = 12345
        _execute.return_value = [
            ("COMP", "DESC", id_orgao, 10),
            ("COMP", "DESC", id_orgao, 11),
        ]

        data = dao.ResumoAlertasComprasDAO.get(id_orgao=id_orgao)
        expected = [
            {
                "sigla": "COMP",
                "descricao": "DESC",
                "orgao": id_orgao,
                "count": 10,
            },
            {
                "sigla": "COMP",
                "descricao": "DESC",
                "orgao": id_orgao,
                "count": 11,
            }
        ]

        self.assertEqual(data, expected)


class ResumoAlertasDAOTest(TestCase):
    def setUp(self):
        self.orgao_id = '12345'

        self.exec_mgp_dao_patcher = mock.patch.object(
            dao.ResumoAlertasMGPDAO,
            "execute"
        )
        self.exec_compras_dao_patcher = mock.patch.object(
            dao.ResumoAlertasComprasDAO,
            "execute"
        )
        self.execute_mgp_dao_mock = self.exec_mgp_dao_patcher.start()
        self.execute_compras_dao_mock = self.exec_compras_dao_patcher.start()
        self.execute_compras_dao_mock.return_value = [
            ("Compras 1", "mock 1", self.orgao_id, 10),
            ("Compras 2", "mock 2", self.orgao_id, 11),
        ]
        self.execute_mgp_dao_mock.return_value = [
            ("MGP 1", "mock 3", self.orgao_id, 12),
            ("MGP 2", "mock 4", self.orgao_id, 13),
        ]
        self.expected = [
            {
                'sigla': 'MGP 1',
                'descricao': 'mock 3',
                'orgao': 12345,
                'count': 12,
            },
            {
                'sigla': 'MGP 2',
                'descricao': 'mock 4',
                'orgao': 12345,
                'count': 13,
            },
            {
                'sigla': 'Compras 1',
                'descricao': 'mock 1',
                'orgao': 12345,
                'count': 10,
            },
            {
                'sigla': 'Compras 2',
                'descricao': 'mock 2',
                'orgao': 12345,
                'count': 11
            },
        ]

    def tearDown(self):
        self.exec_mgp_dao_patcher.stop()
        self.exec_compras_dao_patcher.stop()

    def test_get_all_data(self):
        resumo = dao.ResumoAlertasDAO.get_all(id_orgao=self.orgao_id)

        self.assertEqual(resumo, self.expected)

    def test_get_all_data_accept_empty_resumo_compras(self):
        self.execute_compras_dao_mock.return_value = []
        resumo = dao.ResumoAlertasDAO.get_all(id_orgao=self.orgao_id)

        expected = self.expected[:2]
        self.assertEqual(resumo, expected)

    def test_get_all_data_accept_empty_resumo_mgp(self):
        self.execute_mgp_dao_mock.return_value = []
        resumo = dao.ResumoAlertasDAO.get_all(id_orgao=self.orgao_id)

        expected = self.expected[2:]
        self.assertEqual(resumo, expected)
