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
            ("COMP", "mock 1", self.orgao_id, 10),
            ("COMP", "mock 2", self.orgao_id, 11),
        ]
        self.execute_mgp_dao_mock.return_value = [
            ("GATE", "mock 3", self.orgao_id, 12),
            ("PRCR", "mock 4", self.orgao_id, 13),
        ]
        self.expected = [
            {
                'sigla': 'PRCR',
                'descricao': 'mock 4',
                'orgao': 12345,
                'count': 13,
            },
            {
                'sigla': 'COMP',
                'descricao': 'mock 1',
                'orgao': 12345,
                'count': 10,
            },
            {
                'sigla': 'COMP',
                'descricao': 'mock 2',
                'orgao': 12345,
                'count': 11,
            },
            {
                'sigla': 'GATE',
                'descricao': 'mock 3',
                'orgao': 12345,
                'count': 12
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

        expected = [self.expected[0], self.expected[3]]
        self.assertEqual(resumo, expected)

    def test_get_all_data_accept_empty_resumo_mgp(self):
        self.execute_mgp_dao_mock.return_value = []
        resumo = dao.ResumoAlertasDAO.get_all(id_orgao=self.orgao_id)

        expected = self.expected[1:3]
        self.assertEqual(resumo, expected)


class TestAlertaMGPDAO(TestCase):
    def setUp(self):
        self.run_query_patcher = mock.patch("dominio.alertas.dao.run_query")
        self.run_query_mock = self.run_query_patcher.start()

    def tearDown(self):
        self.run_query_patcher.stop()

    def test_validos_por_orgaos(self):
        orgao_id = 12345
        self.run_query_mock.return_value = [
            (
                'data 1',
                'data 2',
                0,
                'data 3',
                'data 4',
                'data 5',
                'data 6',
                'data 7',
                int(orgao_id),
                'data 8',
                'COMP',
            )
        ]
        resp = dao.AlertaMGPDAO.get(orgao_id=orgao_id)
        expected_resp = [
            {
                'doc_dk': 'data 1',
                'num_doc': 'data 2',
                'num_ext': 0,
                'etiqueta': 'data 3',
                'classe_doc': 'data 4',
                'data_alerta': 'data 5',
                'orgao': 'data 6',
                'classe_hier': 'data 7',
                'dias_passados': 12345,
                'descricao': 'data 8',
                'sigla': 'COMP'}
        ]

        self.run_query_mock.assert_called_once_with(
            dao.AlertaMGPDAO.query(),
            {"orgao_id": orgao_id},
        )
        self.assertEqual(resp, expected_resp)

    def test_validos_por_orgaos_tipo(self):
        orgao_id = 12345
        tipo_alerta = 'ALRT'
        self.run_query_mock.return_value = [
            (
                'data 1',
                'data 2',
                0,
                'data 3',
                'data 4',
                'data 5',
                'data 6',
                'data 7',
                int(orgao_id),
                'data 8',
                'DORD',
            ),
            (
                'data 1',
                'data 2',
                0,
                'data 3',
                'data 4',
                'data 5',
                'data 6',
                'data 7',
                int(orgao_id),
                'data 8',
                'COMP',
            ),
        ]
        resp = dao.AlertaMGPDAO.get(orgao_id=orgao_id, tipo_alerta=tipo_alerta)
        expected_resp = [
            {
                'doc_dk': 'data 1',
                'num_doc': 'data 2',
                'num_ext': 0,
                'etiqueta': 'data 3',
                'classe_doc': 'data 4',
                'data_alerta': 'data 5',
                'orgao': 'data 6',
                'classe_hier': 'data 7',
                'dias_passados': 12345,
                'descricao': 'data 8',
                'sigla': 'COMP'
            },
            {
                'doc_dk': 'data 1',
                'num_doc': 'data 2',
                'num_ext': 0,
                'etiqueta': 'data 3',
                'classe_doc': 'data 4',
                'data_alerta': 'data 5',
                'orgao': 'data 6',
                'classe_hier': 'data 7',
                'dias_passados': 12345,
                'descricao': 'data 8',
                'sigla': 'DORD'
            }
        ]

        cls = dao.AlertaMGPDAO
        with open(
            cls.QUERIES_DIR.child("validos_por_orgao_tipo.sql")
        ) as fobj:
            expected_query = fobj.read()

        expected_query = expected_query.format(**cls.table_namespaces)

        self.run_query_mock.assert_called_once_with(
            expected_query,
            {"orgao_id": orgao_id, "tipo_alerta": tipo_alerta},
        )
        self.assertEqual(resp, expected_resp)
