from datetime import datetime
from unittest import mock

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from dominio.documentos.views import BaseDocumentoViewMixin
from dominio.exceptions import APIEmptyResultError
from dominio.tests.testconf import NoJWTTestCase


class TestBaseDocumentoViewMixin(TestCase):
    def test_create_response(self):
        expected_cont_type = (
            "Content-Type",
            'application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document'
        )
        attachment_name = "attachment.docx"
        expected_disposition = (
            "Content-Disposition",
            f"attachment;filename={attachment_name}"
        )

        class ChildClassView(BaseDocumentoViewMixin):
            attachment_name = "attachment.docx"

        resp = ChildClassView().create_response()

        headers = resp._headers
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(headers["content-type"], expected_cont_type)
        self.assertEqual(
            headers["content-disposition"],
            expected_disposition
        )


class TestDownloadMinutaPrescricao(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.orgao_id = 56789
        self.cpf = "1234567890"
        self.docu_dk = 12345
        self.url = reverse(
            "dominio:minuta-prescricao",
            args=(self.orgao_id, self.cpf, self.docu_dk)
        )

        self.cont_patcher = mock.patch(
            "dominio.documentos.views.MinutaPrescricaoController"
        )
        self.controller_mock = self.cont_patcher.start()
        self.minuta_controller_mock = mock.Mock()
        self.controller_mock.return_value = self.minuta_controller_mock

    def tearDown(self):
        super().tearDown()
        self.cont_patcher.stop()

    def test_correct_response(self):
        resp = self.client.get(self.url)

        expected_cont_type = (
            "Content-Type",
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )

        self.assertEqual(resp.status_code, 200)
        self.controller_mock.assert_called_once_with(
            orgao_id=self.orgao_id,
            cpf=self.cpf,
            docu_dk=self.docu_dk,
        )
        self.minuta_controller_mock.render.assert_called_once()
        self.assertIsInstance(
            self.minuta_controller_mock.render.call_args_list[0][0][0],
            HttpResponse
        )
        self.assertEqual(resp._headers["content-type"], expected_cont_type)

    def test_404_for_empty_db_response(self):
        self.minuta_controller_mock.render.side_effect = APIEmptyResultError
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 404)


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

    def test_404_for_empty_db_response(self):
        self.controller_mock.render.side_effect = APIEmptyResultError
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 404)


class TestProrrogacaoPp(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()

        self.orgao_id = 12345
        self.docu_dk = 4567
        self.cpf = "0000000"
        self.url = reverse(
            "dominio:prorrogacao-pp",
            args=(self.orgao_id, self.cpf, self.docu_dk)
        )

        self.cont_prorrogacao_patcher = mock.patch(
            "dominio.documentos.views.ProrrogacaoPPController"
        )
        self.controller_mock = mock.Mock()
        self.cont_prorrogacao_mock = self.cont_prorrogacao_patcher.start()
        self.cont_prorrogacao_mock.return_value = self.controller_mock

    def tearDown(self):
        super().tearDown()
        self.cont_prorrogacao_patcher.stop()

    def test_correct_response(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.cont_prorrogacao_mock.assert_called_once_with(
            orgao_id=self.orgao_id,
            cpf=self.cpf,
            docu_dk=self.docu_dk,
        )
        self.assertIsInstance(
            self.controller_mock.render.call_args_list[0][0][0],
            HttpResponse
        )

    def test_404_for_empty_db_response(self):
        self.controller_mock.render.side_effect = APIEmptyResultError
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 404)


class TestInstauracaoIC(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()

        self.orgao_id = 12345
        self.docu_dk = 4567
        self.cpf = "0000000"
        self.url = reverse(
            "dominio:instauracao-ic",
            args=(self.orgao_id, self.cpf, self.docu_dk)
        )

        self.cont_instauracao_patcher = mock.patch(
            "dominio.documentos.views.InstauracaoICController"
        )
        self.controller_mock = mock.Mock()
        self.cont_instauracao_mock = self.cont_instauracao_patcher.start()
        self.cont_instauracao_mock.return_value = self.controller_mock

    def tearDown(self):
        super().tearDown()
        self.cont_instauracao_patcher.stop()

    def test_correct_response(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.cont_instauracao_mock.assert_called_once_with(
            orgao_id=self.orgao_id,
            cpf=self.cpf,
            docu_dk=self.docu_dk,
        )
        self.assertIsInstance(
            self.controller_mock.render.call_args_list[0][0][0],
            HttpResponse
        )

    def test_404_for_empty_db_response(self):
        self.controller_mock.render.side_effect = APIEmptyResultError
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 404)


class TestListaROsAusentes(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.num_delegacia = 12
        self.url = reverse("dominio:ros-ausentes", args=(self.num_delegacia,))

        self.dao_exec_patcher = mock.patch(
            "dominio.documentos.views.ListaROsAusentesDAO.execute"
        )
        self.dao_exec_mock = self.dao_exec_patcher.start()
        self.dao_exec_mock.return_value = [
            (1,),
            (2,),
            (5,),
        ]

    def tearDown(self):
        super().tearDown()
        self.dao_exec_mock.stop()

    def test_correct_response(self):
        resp = self.client.get(self.url)

        headers = resp._headers
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            headers["content-type"],
            (
                "Content-Type",
                "application/vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            )
        )
        self.assertEqual(
            headers["content-disposition"],
            (
                'Content-Disposition',
                'attachment; '
                f'filename="dp-{self.num_delegacia}-ros-ausentes.xlsx"'
            )
        )


class TestListaProcessosBaixaDP(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.orgao_id = 12345
        self.url = reverse("dominio:baixa-dp", args=(self.orgao_id,))

        self.dao_exec_patcher = mock.patch(
            "dominio.documentos.views.ListaProcessosBaixaDPDAO.execute"
        )
        self.dao_exec_mock = self.dao_exec_patcher.start()
        self.dao_exec_mock.return_value = [
            ("numero processo 1", "orgao baixa 1", datetime(2020, 1, 1)),
            ("numero processo 2", "orgao baixa 2", datetime(2020, 1, 2)),
            ("numero processo 3", "orgao baixa 3", datetime(2020, 1, 3)),
        ]

    def tearDown(self):
        super().tearDown()
        self.dao_exec_mock.stop()

    def test_correct_response(self):
        resp = self.client.get(self.url)

        headers = resp._headers
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            headers["content-type"],
            (
                "Content-Type",
                "application/vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            )
        )
        self.assertEqual(
            headers["content-disposition"],
            (
                'Content-Disposition',
                'attachment; '
                f'filename="processos-com-baixa-dp.xlsx"'
            )
        )


class TestComunicacaoCSMP(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()

        self.orgao_id = 12345
        self.cpf = "0000000"
        self.url = reverse(
            "dominio:procedimentos-csmp",
            args=(self.orgao_id, self.cpf)
        )

        self.cont_instauracao_patcher = mock.patch(
            "dominio.documentos.views.ComunicacaoCSMPController"
        )
        self.controller_mock = mock.Mock()
        self.cont_instauracao_mock = self.cont_instauracao_patcher.start()
        self.cont_instauracao_mock.return_value = self.controller_mock

    def tearDown(self):
        super().tearDown()
        self.cont_instauracao_patcher.stop()

    def test_correct_response(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.cont_instauracao_mock.assert_called_once_with(
            orgao_id=self.orgao_id,
            cpf=self.cpf
        )
        self.assertIsInstance(
            self.controller_mock.render.call_args_list[0][0][0],
            HttpResponse
        )

    def test_404_for_empty_db_response(self):
        self.controller_mock.render.side_effect = APIEmptyResultError
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 404)
