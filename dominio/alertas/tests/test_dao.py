from unittest import mock
import pytest

from django.test import TestCase

from dominio.alertas import dao
from dominio.alertas.exceptions import (
    APIInvalidOverlayType,
    APIMissingOverlayType,
)


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
                'id_comp',
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
                'id_alerta': 'id_comp',
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
                'id_dord',
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
                'id_comp',
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
                'id_alerta': 'id_comp',
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
                'id_alerta': 'id_dord',
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


class TestFiltraAlertasDispensados(TestCase):
    def setUp(self):
        self.orgao_id = "12345"
        self.get_hbase_table_patcher = mock.patch.object(
            dao.FiltraAlertasDispensadosMixin, "get_table"
        )
        self.get_hbase_table_mock = self.get_hbase_table_patcher.start()

        self.table_mock = mock.Mock()
        self.dados_hbase = [
            (
                b"key 1",
                {
                    b"dados_alertas:alerta_id": b"12345",
                    b"dados_alertas:orgao": self.orgao_id.encode(),
                    b"dados_alertas:sigla": b"COMP"
                }
            ),
            (
                b"key 2",
                {
                    b"dados_alertas:alerta_id": b"bbbbb-12345",
                    b"dados_alertas:orgao": self.orgao_id.encode(),
                    b"dados_alertas:sigla": b"COMP"
                }
            )
        ]
        self.table_mock.scan.return_value = self.dados_hbase
        self.get_hbase_table_mock.return_value = self.table_mock

        self.get_patcher = mock.patch.object(dao.AlertasDAO, "get")
        self.get_mock = self.get_patcher.start()

        self.alertas = [
            {
                'sigla': 'COMP',
                'contrato': 'aaaa',
                'iditem': 87654,
                'contrato_iditem': 'aaaa-87654',
                'item': 'item desc',
            },
            {
                'sigla': 'COMP',
                'contrato': 'bbbbb',
                'iditem': 12345,
                'contrato_iditem': 'bbbbb-12345',
                'item': 'item desc',
            },
        ]
        self.get_mock.return_value = self.alertas
        self.expected_filtrados = self.alertas[:1]

    def tearDown(self):
        self.get_hbase_table_patcher.stop()
        self.get_patcher.stop()

    def test_prepara_dados_hbase(self):
        prep_hbase = dao.FiltraAlertasDispensadosMixin.prepara_dados_hbase(
            self.dados_hbase
        )
        expected = [("COMP", "12345"), ("COMP", "bbbbb-12345")]

        self.assertEqual(prep_hbase, expected)

    def test_filtra_alertas_dispensados(self):
        class AlertaMock(dao.FiltraAlertasDispensadosMixin, dao.AlertasDAO):
            orgao_kwarg = "id_orgao"
            alerta_id_kwarg = "contrato_iditem"
            sigla_kwarg = "sigla"

        resp = AlertaMock.get(id_orgao=self.orgao_id)

        self.table_mock.scan.assert_called_once_with(
            row_prefix=f"{self.orgao_id}".encode()
        )
        self.assertEqual(resp, self.expected_filtrados)


class TestAlertasOverlayDAO(TestCase):
    @mock.patch.object(dao.AlertasOverlayDAO, "switcher")
    def test_get_result_OK(self, _switcher):
        mock_DAO = mock.MagicMock()
        mock_DAO.get.return_value = [{'data': 1}]
        _switcher.return_value = mock_DAO

        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste_tipo'}

        expected_output = [{'data': 1}]
        docu_dk = 10

        output = dao.AlertasOverlayDAO.get(docu_dk, mock_request)

        _switcher.assert_called_once_with('teste_tipo')
        mock_DAO.get.assert_called_once_with(
            docu_dk=docu_dk,
            request=mock_request
        )
        self.assertEqual(output, expected_output)

    def test_get_no_type(self):
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        docu_dk = 10

        with pytest.raises(APIMissingOverlayType):
            dao.AlertasOverlayDAO.get(docu_dk, mock_request)

    def test_get_invalid_type(self):
        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste_tipo'}

        docu_dk = 10

        with pytest.raises(APIInvalidOverlayType):
            dao.AlertasOverlayDAO.get(docu_dk, mock_request)

    def test_overlay_prescricao(self):
        pass
        # _execute.return_value = [
        #     ('Crime1', 'Nome1', '1.0', 'Nomes',
        #      '0.5', '0.5', '2020-01-01', '2020-01-02'),
        #     ('Crime2', 'Nome1', '1.0', 'Nomes',
        #      '0.5', '0.5', '2020-02-01', '2020-02-02'),
        # ]

        # alertas_expected = [
        #     {
        #         'tipo_penal': 'Crime1',
        #         'nm_investigado': 'Nome1',
        #         'max_pena': 1.0,
        #         'delitos_multiplicadores': 'Nomes',
        #         'fator_pena': 0.5,
        #         'max_pena_fatorado': 0.5,
        #         'dt_inicio_prescricao': '2020-01-01',
        #         'dt_fim_prescricao': '2020-01-02'
        #     },
        #     {
        #         'tipo_penal': 'Crime2',
        #         'nm_investigado': 'Nome1',
        #         'max_pena': 1.0,
        #         'delitos_multiplicadores': 'Nomes',
        #         'fator_pena': 0.5,
        #         'max_pena_fatorado': 0.5,
        #         'dt_inicio_prescricao': '2020-02-01',
        #         'dt_fim_prescricao': '2020-02-02'
        #     },
        # ]
