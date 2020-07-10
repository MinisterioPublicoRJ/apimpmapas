from unittest import mock
from unittest.mock import ANY

from django.test import TestCase
from django.urls import reverse

from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


class SuaMesaViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.suamesa.views.SuaMesaDAO.get")
    def test_correct_response_get(self, _get_data):
        _get_data.return_value = {"data": 1}

        url = reverse(
            "dominio:suamesa-documentos",
            args=("123456",)
        )
        resp = self.client.get(url)

        _get_data.assert_called_once_with(123456, ANY)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {"data": 1})


class SuaMesaDetalheViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.suamesa.views.SuaMesaDetalheFactoryDAO.get")
    def test_correct_response_get(self, _get_data):
        _get_data.return_value = {"data": 1}

        url = reverse(
            "dominio:suamesa-documentos-detalhe",
            args=("123456",)
        )
        resp = self.client.get(url)

        _get_data.assert_called_once_with(123456, ANY)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {"data": 1})
