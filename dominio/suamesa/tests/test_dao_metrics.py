from unittest import mock
import pytest

from django.test import TestCase

from dominio.dao import SingleDataObjectDAO
from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase
from dominio.suamesa.dao_metrics import MetricsDataObjectDAO
from dominio.suamesa.exceptions import APIMissingRequestParameterSuaMesa


class TestMetricsDataObjectDAO(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.suamesa.dao_metrics."
                "MetricsDataObjectDAO.required_parameters",
                new_callable=mock.PropertyMock)
    def test_check_required_parameters_OK(self, _required_parameters):
        _required_parameters.return_value = ['p']

        mock_request = mock.MagicMock()
        mock_request.GET = {'p': 'definido'}

        MetricsDataObjectDAO.check_required_parameters(mock_request)

    @mock.patch("dominio.suamesa.dao_metrics."
                "MetricsDataObjectDAO.required_parameters",
                new_callable=mock.PropertyMock)
    def test_check_required_parameters_missing(self, _required_parameters):
        _required_parameters.return_value = ['p']

        mock_request = mock.MagicMock()
        mock_request.GET = {}

        with pytest.raises(APIMissingRequestParameterSuaMesa):
            MetricsDataObjectDAO.check_required_parameters(mock_request)

    @mock.patch.object(SingleDataObjectDAO, "get")
    def test_get_has_data(self, _get):
        _get.return_value = {'data': 1}

        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste'}

        orgao_id = 10
        kwargs = {
            'orgao_id': 10,
            'tipo_detalhe': 'teste',
            'cpf': None,
            'intervalo': 'mes',
        }

        output = MetricsDataObjectDAO.get(orgao_id, mock_request)

        self.assertEqual(output, {'metrics': {'data': 1}})
        _get.assert_called_once_with(accept_empty=True, **kwargs)

    @mock.patch.object(SingleDataObjectDAO, "get")
    def test_get_has_no_data_accept(self, _get):
        _get.return_value = {}

        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste'}

        orgao_id = 10
        kwargs = {
            'orgao_id': 10,
            'tipo_detalhe': 'teste',
            'cpf': None,
            'intervalo': 'mes',
        }

        output = MetricsDataObjectDAO.get(orgao_id, mock_request)

        self.assertEqual(output, {'metrics': {}})
        _get.assert_called_once_with(accept_empty=True, **kwargs)

    @mock.patch.object(SingleDataObjectDAO, "get")
    def test_get_has_no_data_not_accept(self, _get):
        _get.return_value = {}

        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste'}

        orgao_id = 10
        kwargs = {
            'orgao_id': 10,
            'tipo_detalhe': 'teste',
            'cpf': None,
            'intervalo': 'mes',
        }

        output = MetricsDataObjectDAO.get(
            orgao_id,
            mock_request,
            accept_empty=False
        )

        self.assertEqual(output, {'metrics': {}})
        _get.assert_called_once_with(accept_empty=False, **kwargs)
