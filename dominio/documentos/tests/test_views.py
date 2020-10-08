from unittest import mock

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from dominio.documentos.views import MinutaPrescricaoView
from dominio.tests.testconf import NoJWTTestCase


class TestDownloadMinutaPrescricao(NoJWTTestCase, TestCase):

    def setUp(self):
        super().setUp()
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

        orgao_id = 56789
        docu_dk = 12345
        cpf = "1234567890"
        url = reverse(
            "dominio:minuta-prescricao",
            args=(orgao_id, cpf, docu_dk)
        )
        resp = self.client.get(url)

        expected_cont_type = (
            "Content-Type",
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )

        self.assertEqual(resp.status_code, 200)
        _controller.assert_called_once_with(
            orgao_id=orgao_id,
            cpf=cpf,
            docu_dk=docu_dk,
        )
        minuta_controller_mock.render.assert_called_once()
        self.assertIsInstance(
            minuta_controller_mock.render.call_args_list[0][0][0],
            HttpResponse
        )
        self.assertEqual(resp._headers["content-type"], expected_cont_type)


class TestProrrogacaoIC(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()

        self.orgao_id = 12345
        self.docu_dk = 4567
        self.cpf = "0000000"
        self.url = reverse(
            "dominio:prorrogacao-ic",
            args=(self.orgao_id, self.cpf, self.docu_dk)
        )

        self.cont_prorrogacao_patcher = mock.patch(
            "dominio.documentos.views.ProrrogacaoICController"
        )
        self.controller_mock = mock.Mock()
        self.cont_prorrogacao_mock = self.cont_prorrogacao_patcher.start()
        self.cont_prorrogacao_mock.return_value = self.controller_mock

    def tearDown(self):
        super().tearDown()
        self.cont_prorrogacao_patcher.stop()

    def test_correct_response(self):
        resp = self.client.get(self.url)

        self.cont_prorrogacao_mock.assert_called_once_with(
            orgao_id=self.orgao_id,
            cpf=self.cpf,
            docu_dk=self.docu_dk,
        )
        self.assertEqual(resp.status_code, 200)
        self.controller_mock.render_assert_called()
        self.assertIsInstance(
            self.controller_mock.render.call_args_list[0][0][0],
            HttpResponse
        )
