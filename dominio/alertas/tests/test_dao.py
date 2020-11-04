from unittest import mock
import pytest

from django.test import TestCase
from django.core.cache import cache

from dominio.alertas import dao
from dominio.alertas.exceptions import (
    APIInvalidOverlayType,
    APIMissingOverlayType,
)


class AlertaMaxPartitionDAOTest(TestCase):
    @mock.patch.object(dao.AlertaMaxPartitionDAO, "execute")
    def test_get_data(self, _execute):
        _execute.return_value = [('20201010',)]
        data = dao.AlertaMaxPartitionDAO.get()
        expected = '20201010'

        cache.clear()
        self.assertEqual(data, expected)

    @mock.patch.object(dao.AlertaMaxPartitionDAO, "execute")
    def test_get_no_data(self, _execute):
        _execute.return_value = []
        data = dao.AlertaMaxPartitionDAO.get()
        expected = '-1'

        self.assertEqual(data, expected)


class ResumoAlertasDAOTest(TestCase):
    def setUp(self):
        self.orgao_id = '12345'

        self.exec_mgp_dao_patcher = mock.patch.object(
            dao.ResumoAlertasDAO,
            "execute"
        )
        self.execute_mgp_dao_mock = self.exec_mgp_dao_patcher.start()
        self.execute_mgp_dao_mock.return_value = [
            ("COMP", 10),
            ("COMP", 11),
            ("GATE", 12),
            ("PRCR", 13),
        ]
        self.exec_max_partition_dao_patcher = mock.patch.object(
            dao.AlertaMaxPartitionDAO,
            "get"
        )
        self.max_pt_dao_mock = self.exec_max_partition_dao_patcher.start()
        self.max_pt_dao_mock.return_value = '20201010'

        self.expected = [
            {
                'sigla': 'PRCR',
                'count': 13,
            },
            {
                'sigla': 'COMP',
                'count': 10,
            },
            {
                'sigla': 'COMP',
                'count': 11,
            },
            {
                'sigla': 'GATE',
                'count': 12
            },
        ]

    def tearDown(self):
        self.exec_mgp_dao_patcher.stop()
        self.exec_max_partition_dao_patcher.stop()

    def test_get_all_data(self):
        resumo = dao.ResumoAlertasDAO.get_all(id_orgao=self.orgao_id)

        self.assertEqual(resumo, self.expected)


class TestAlertaMGPDAO(TestCase):
    def setUp(self):
        self.exec_mgp_dao_patcher = mock.patch.object(
            dao.AlertaMGPDAO,
            "execute"
        )
        self.run_query_mock = self.exec_mgp_dao_patcher.start()

        self.exec_max_partition_dao_patcher = mock.patch.object(
            dao.AlertaMaxPartitionDAO,
            "get"
        )
        self.max_pt_dao_mock = self.exec_max_partition_dao_patcher.start()
        self.max_pt_dao_mock.return_value = '20201010'

    def tearDown(self):
        self.exec_mgp_dao_patcher.stop()
        self.exec_max_partition_dao_patcher.stop()

    def test_validos_por_orgaos(self):
        orgao_id = 12345
        self.run_query_mock.return_value = [
            (
                1,
                'data 1',
                'data 2',
                orgao_id,
                1,
                'id_comp',
                'COMP',
            )
        ]
        resp = dao.AlertaMGPDAO.get(orgao_id=orgao_id)
        expected_resp = [
            {
                'doc_dk': 1,
                'num_doc': 'data 1',
                'data_alerta': 'data 2',
                'orgao': orgao_id,
                'dias_passados': 1,
                'id_alerta': 'id_comp',
                'sigla': 'COMP'
            }
        ]

        self.run_query_mock.assert_called_once_with(
            orgao_id=orgao_id, dt_partition='20201010'
        )
        self.assertEqual(resp, expected_resp)

    def test_validos_por_orgaos_tipo(self):
        orgao_id = 12345
        tipo_alerta = 'ALRT'
        self.run_query_mock.return_value = [
            (
                1,
                'data 1',
                'data 2',
                orgao_id,
                1,
                'id_dord',
                'DORD',
            ),
            (
                1,
                'data 1',
                'data 2',
                orgao_id,
                1,
                'id_comp',
                'COMP',
            ),
        ]
        resp = dao.AlertaMGPDAO.get(orgao_id=orgao_id, tipo_alerta=tipo_alerta)
        expected_resp = [
            {
                'doc_dk': 1,
                'num_doc': 'data 1',
                'data_alerta': 'data 2',
                'orgao': orgao_id,
                'dias_passados': 1,
                'id_alerta': 'id_comp',
                'sigla': 'COMP'
            },
            {
                'doc_dk': 1,
                'num_doc': 'data 1',
                'data_alerta': 'data 2',
                'orgao': orgao_id,
                'dias_passados': 1,
                'id_alerta': 'id_dord',
                'sigla': 'DORD'
            }
        ]

        self.run_query_mock.assert_called_once_with(
            orgao_id=orgao_id,
            tipo_alerta=tipo_alerta,
            dt_partition='20201010'
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

    def test_create_hbase_query(self):
        hbase_query = dao.FiltraAlertasDispensadosMixin.prepara_hbase_query(
            self.orgao_id
        )

        expected = (
            "SingleColumnValueFilter('dados_alertas', 'orgao', =,"
            f" 'binary:{self.orgao_id}')"
            " OR SingleColumnValueFilter('dados_alertas', 'orgao', =,"
            " 'binary:ALL')"
        ).encode()

        self.assertEqual(hbase_query, expected)

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
        expected_hbase_query = AlertaMock.prepara_hbase_query(self.orgao_id)

        self.table_mock.scan.assert_called_once_with(
            filter=expected_hbase_query
        )
        self.assertEqual(resp, self.expected_filtrados)


class TestAlertasOverlayDAO(TestCase):
    @mock.patch.object(dao.AlertaMaxPartitionDAO, "get")
    @mock.patch.object(dao.AlertasOverlayDAO, "switcher")
    def test_get_result_OK(self, _switcher, _dt_partition):
        mock_DAO = mock.MagicMock()
        mock_DAO.get.return_value = [{'data': 1}]
        _switcher.return_value = mock_DAO

        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste_tipo'}

        expected_output = [{'data': 1}]
        docu_dk = 10

        _dt_partition.return_value = '20201010'

        output = dao.AlertasOverlayDAO.get(docu_dk, mock_request)

        _switcher.assert_called_once_with('teste_tipo')
        mock_DAO.get.assert_called_once_with(
            docu_dk=docu_dk,
            dt_partition='20201010'
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

    @mock.patch("dominio.dao.impala_execute")
    def test_overlay_prescricao(self, _execute):
        _execute.return_value = [
            ('Crime1', 'Nome1', '1.0', 'Nomes',
             '0.5', '0.5', '2020-01-01', '2020-01-02', '1_2_3'),
            ('Crime2', 'Nome1', '1.0', 'Nomes',
             '0.5', '0.5', '2020-02-01', '2020-02-02', '4_5_6'),
        ]

        alertas_expected = [
            {
                'tipo_penal': 'Crime1',
                'nm_investigado': 'Nome1',
                'max_pena': 1.0,
                'delitos_multiplicadores': 'Nomes',
                'fator_pena': 0.5,
                'max_pena_fatorado': 0.5,
                'dt_inicio_prescricao': '2020-01-01',
                'dt_fim_prescricao': '2020-01-02',
                'adpr_chave': '1_2_3'
            },
            {
                'tipo_penal': 'Crime2',
                'nm_investigado': 'Nome1',
                'max_pena': 1.0,
                'delitos_multiplicadores': 'Nomes',
                'fator_pena': 0.5,
                'max_pena_fatorado': 0.5,
                'dt_inicio_prescricao': '2020-02-01',
                'dt_fim_prescricao': '2020-02-02',
                'adpr_chave': '4_5_6'
            },
        ]

        docu_dk = 10
        mock_request = mock.MagicMock()

        data = dao.AlertaOverlayPrescricaoDAO.get(
            docu_dk=docu_dk, request=mock_request
        )
        self.assertEqual(data, alertas_expected)


class TestFiltraAlertasDispensadosTodosOrgaos(TestCase):
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
            ),
            (
                b"key 3",
                {
                    b"dados_alertas:alerta_id": b"cccc-12345",
                    b"dados_alertas:orgao": "ALL",
                    b"dados_alertas:sigla": b"COMP"
                }
            ),
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
            {
                'sigla': 'COMP',
                'contrato': 'ccccc',
                'iditem': 12345,
                'contrato_iditem': 'cccc-12345',
                'item': 'item desc',
            },
        ]
        self.get_mock.return_value = self.alertas
        self.expected_filtrados = self.alertas[:1]

    def tearDown(self):
        self.get_hbase_table_patcher.stop()
        self.get_patcher.stop()

    def test_filtra_alertas_dispensados(self):
        class AlertaMock(dao.FiltraAlertasDispensadosMixin, dao.AlertasDAO):
            orgao_kwarg = "id_orgao"
            alerta_id_kwarg = "contrato_iditem"
            sigla_kwarg = "sigla"

        resp = AlertaMock.get(id_orgao=self.orgao_id)
        expected_hbase_query = AlertaMock.prepara_hbase_query(self.orgao_id)

        self.table_mock.scan.assert_called_once_with(
            filter=expected_hbase_query
        )
        self.assertEqual(resp, self.expected_filtrados)


class TestDetalheAlertaCompras(TestCase):
    def setUp(self):
        self.alerta_id = "abc1234"
        self.query_exec_patcher = mock.patch.object(
            dao.DetalheAlertaCompraDAO, "execute"
        )
        self.query_exec_mock = self.query_exec_patcher.start()
        self.query_exec_mock.return_value = (
            (
                "12345",
                "01/01/2020",
                "56789",
                123.34,
            ),
        )
        self.expected_data = {
            "contratacao": "12345",
            "data_contratacao": "01/01/2020",
            "item_contratado": "56789",
            "var_perc": "123,34"
        }

    def tearDown(self):
        self.query_exec_patcher.stop()

    def test_get_detalhe_alerta(self):
        data = dao.DetalheAlertaCompraDAO.get(alerta_id=self.alerta_id)

        self.assertEqual(data, self.expected_data)
