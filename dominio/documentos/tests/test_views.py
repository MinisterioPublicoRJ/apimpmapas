from unittest import mock

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from dominio.documentos.views import MinutaPrescricaoView
from dominio.tests.testconf import NoJWTTestCase


class TestDownloadMinutaPrescricao(NoJWTTestCase, TestCase):

    def setUp(self):
        super().setUp()
        self.mock_jwt.return_value = {
            "matricula": "12345678"
        }
        self. expected_cont_type = (
            "Content-Type",
            'application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document'
        )
        self.expected_disposition = (
            "Content-Disposition",
            "attachment;filename=minuta-prescricao.docx"
        )

    def test_create_response(self):
        resp = MinutaPrescricaoView().create_response()

        headers = resp._headers
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(headers["content-type"], self.expected_cont_type)
        self.assertEqual(
            headers["content-disposition"],
            self.expected_disposition
        )

    @mock.patch("dominio.documentos.views.MinutaPrescricaoController")
    def test_correct_response(self, _controller):
        minuta_controller_mock = mock.Mock()
        _controller.return_value = minuta_controller_mock

        docu_dk = 12345
        url = reverse("dominio:minuta-prescricao", args=(docu_dk,))
        resp = self.client.get(url)

        expected_cont_type = (
            "Content-Type",
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )

        self.assertEqual(resp.status_code, 200)
        _controller.assert_called_once_with(
            docu_dk,
            self.mock_jwt.return_value
        )
        minuta_controller_mock.render.assert_called_once()
        self.assertIsInstance(
            minuta_controller_mock.render.call_args_list[0][0][0],
            HttpResponse
        )
        self.assertEqual(resp._headers["content-type"], expected_cont_type)
