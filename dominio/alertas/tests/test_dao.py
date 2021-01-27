from unittest import mock
import pytest

from django.test import TestCase

from dominio.alertas import dao
from dominio.alertas.exceptions import (
    APIInvalidOverlayType,
    APIMissingOverlayType,
)


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

    def test_get_all_data(self):
        resumo = dao.ResumoAlertasDAO.get_all(id_orgao=self.orgao_id)

        self.assertEqual(resumo, self.expected)


class TestAlertaMGPDAO(TestCase):
    def setUp(self):
        super().setUp()
        self.exec_mgp_dao_patcher = mock.patch.object(
            dao.AlertaMGPDAO,
            "execute"
        )
        self.run_query_mock = self.exec_mgp_dao_patcher.start()

    def tearDown(self):
        super().tearDown()
        self.exec_mgp_dao_patcher.stop()

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
                'desc',
                'classe',
                'numext',
                'alrtkey',
                0
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
                'sigla': 'COMP',
                'descricao': 'desc',
                'classe_hierarquia': 'classe',
                'num_externo': 'numext',
                'alrt_key': 'alrtkey',
                'flag_dispensado': 0
            }
        ]

        self.run_query_mock.assert_called_once_with(
            orgao_id=orgao_id
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
                'desc',
                'classe',
                'numext',
                'alrtkey',
                0
            ),
            (
                1,
                'data 1',
                'data 2',
                orgao_id,
                1,
                'id_comp',
                'COMP',
                'desc',
                'classe',
                'numext',
                'alrtkey',
                0
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
                'sigla': 'COMP',
                'descricao': 'desc',
                'classe_hierarquia': 'classe',
                'num_externo': 'numext',
                'alrt_key': 'alrtkey',
                'flag_dispensado': 0
            },
            {
                'doc_dk': 1,
                'num_doc': 'data 1',
                'data_alerta': 'data 2',
                'orgao': orgao_id,
                'dias_passados': 1,
                'id_alerta': 'id_dord',
                'sigla': 'DORD',
                'descricao': 'desc',
                'classe_hierarquia': 'classe',
                'num_externo': 'numext',
                'alrt_key': 'alrtkey',
                'flag_dispensado': 0
            }
        ]

        self.run_query_mock.assert_called_once_with(
            orgao_id=orgao_id,
            tipo_alerta=tipo_alerta
        )
        self.assertEqual(resp, expected_resp)


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
            docu_dk=docu_dk
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


class TestDetalheAlertaISPS(TestCase):
    def setUp(self):
        self.alerta_id = "abc1234"
        self.query_exec_patcher = mock.patch.object(
            dao.DetalheAlertaISPSDAO, "execute"
        )
        self.query_exec_mock = self.query_exec_patcher.start()
        self.query_exec_mock.return_value = (
            (
                "NOME MUNICIPIO",
                "DESCRIÇÃO",
            ),
        )
        self.expected_data = {
            "municipio": "NOME MUNICIPIO",
            "descricao": "DESCRIÇÃO",
        }

    def tearDown(self):
        self.query_exec_patcher.stop()

    def test_get_detalhe_alerta(self):
        data = dao.DetalheAlertaISPSDAO.get(alerta_id=self.alerta_id)

        self.assertEqual(data, self.expected_data)
