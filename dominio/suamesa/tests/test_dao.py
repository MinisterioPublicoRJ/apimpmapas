from unittest import mock
import pytest

from django.test import TestCase

from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase
from dominio.suamesa.dao import SuaMesaDAO, SuaMesaDetalheFactoryDAO
from dominio.suamesa.exceptions import (
    APIInvalidSuaMesaType,
    APIMissingSuaMesaType,
)
from dominio.suamesa.dao import SuaMesaDetalhePIPAISPDAO


class TestSuaMesaDAO(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch.object(SuaMesaDAO, "switcher")
    def test_get_result_OK(self, _switcher):
        mock_function = mock.MagicMock()
        mock_function.return_value = 15
        _switcher.return_value = mock_function

        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste_tipo'}

        expected_output = {'nr_documentos': 15}
        orgao_id = 10

        output = SuaMesaDAO.get(orgao_id, mock_request)

        _switcher.assert_called_once_with('teste_tipo')
        mock_function.assert_called_once_with(orgao_id, mock_request)
        self.assertEqual(output, expected_output)

    def test_get_no_type(self):
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        orgao_id = 10

        with pytest.raises(APIMissingSuaMesaType):
            SuaMesaDAO.get(orgao_id, mock_request)

    @mock.patch("dominio.suamesa.dao.SuaMesaDAO._type_switcher",
                new_callable=mock.PropertyMock)
    def test_switcher_result_OK(self, _switcher):
        _switcher.return_value = {'nome_funcao': 'funcao'}
        expected_output = 'funcao'

        output = SuaMesaDAO.switcher('nome_funcao')

        self.assertEqual(output, expected_output)

    @mock.patch("dominio.suamesa.dao.SuaMesaDAO._type_switcher",
                new_callable=mock.PropertyMock)
    def test_switcher_not_valid_type(self, _switcher):
        _switcher.return_value = {'nome_funcao': 'funcao'}

        with pytest.raises(APIInvalidSuaMesaType):
            SuaMesaDAO.switcher('nome_inexistente')


class TestSuaMesaDetalheFactoryDAO(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch.object(SuaMesaDetalheFactoryDAO, "switcher")
    def test_get_result_OK(self, _switcher):
        mock_DAO = mock.MagicMock()
        mock_DAO.get.return_value = {'data': 1}
        _switcher.return_value = mock_DAO

        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste_tipo'}

        expected_output = {'data': 1}
        orgao_id = 10

        output = SuaMesaDetalheFactoryDAO.get(orgao_id, mock_request)

        _switcher.assert_called_once_with('teste_tipo')
        mock_DAO.get.assert_called_once_with(
            orgao_id=orgao_id,
            tipo_detalhe='teste_tipo',
            cpf=None,
            n=3,
            intervalo='mes'
        )
        self.assertEqual(output, expected_output)

    def test_get_no_type(self):
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        orgao_id = 10

        with pytest.raises(APIMissingSuaMesaType):
            SuaMesaDetalheFactoryDAO.get(orgao_id, mock_request)


class TestDetalheAISPDAO(TestCase):
    def setUp(self):
        self.kwargs = {
            'orgao_id': 1234,
            'tipo_detalhe': 'tipo',
            'cpf': '0123',
            'n': 3,
            'intervalo': 'mes'
        }

        self.get_aisps_patcher = mock.patch(
            "dominio.suamesa.dao.get_orgaos_same_aisps"
        )
        self.get_aisps_mock = self.get_aisps_patcher.start()
        self.get_aisps_mock.return_value = (1, {1234})

        self.impala_execute_patcher = mock.patch(
            "dominio.suamesa.dao.impala_execute"
        )
        self.impala_execute_mock = self.impala_execute_patcher.start()

        self.dao_query_patcher = mock.patch.object(
            SuaMesaDetalhePIPAISPDAO,
            "query"
        )
        self.dao_query_mock = self.dao_query_patcher.start()
        self.dao_query_mock.return_value = (
            """
            -- Usando o codigo das pips diretamente (cacheado no back)"""
            """, e não precisa retornar a lista de nomes
            SELECT
                acervo_inicio,
                acervo_fim,
                CASE WHEN (acervo_fim - acervo_inicio) = 0 THEN 0 ELSE """
            """(acervo_fim - acervo_inicio)/acervo_inicio END """
            """as variacao_acervo
            FROM (
                SELECT
                    SUM(acervo_inicio) as acervo_inicio,
                    SUM(acervo_fim) as acervo_fim
                FROM {schema}.tb_detalhe_documentos_orgao
                WHERE tipo_detalhe IN ('pip_inqueritos', 'pip_pics')
                AND intervalo = :intervalo
                AND vist_orgi_orga_dk IN (:orgaos_aisp)
            ) t
        """)
        self.expected_query = (
            """
            -- Usando o codigo das pips diretamente (cacheado no back)"""
            """, e não precisa retornar a lista de nomes
            SELECT
                acervo_inicio,
                acervo_fim,
                CASE WHEN (acervo_fim - acervo_inicio) = 0 THEN 0 ELSE """
            """(acervo_fim - acervo_inicio)/acervo_inicio END """
            """as variacao_acervo
            FROM (
                SELECT
                    SUM(acervo_inicio) as acervo_inicio,
                    SUM(acervo_fim) as acervo_fim
                FROM {schema}.tb_detalhe_documentos_orgao
                WHERE tipo_detalhe IN ('pip_inqueritos', 'pip_pics')
                AND intervalo = :intervalo
                AND vist_orgi_orga_dk IN (:orgao_aisp_0)
            ) t
        """)
        self.expected_kwargs = {
            "orgao_aisp_0": 1234
        }
        self.expected_kwargs.update(self.kwargs)

    def tearDown(self):
        self.get_aisps_patcher.stop()
        self.impala_execute_patcher.stop()
        self.dao_query_patcher.stop()

    def test_prepare_ids_orgaos(self):
        SuaMesaDetalhePIPAISPDAO.execute(**self.kwargs)

        self.impala_execute_mock.assert_called_once_with(
            self.expected_query,
            self.expected_kwargs,
        )
