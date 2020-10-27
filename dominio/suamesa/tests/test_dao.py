from unittest import mock
import pytest

from django.test import TestCase

from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase
from dominio.suamesa.dao import SuaMesaDAO, SuaMesaDetalheFactoryDAO
from dominio.suamesa.exceptions import (
    APIInvalidSuaMesaType,
    APIMissingSuaMesaType,
)


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
