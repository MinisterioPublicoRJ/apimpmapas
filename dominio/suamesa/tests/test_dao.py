from unittest import mock
import pytest

from django.test import TestCase

from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase
from dominio.suamesa.dao import SuaMesaDAO
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
