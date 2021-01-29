from datetime import date
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache

from dominio.alertas import dao
from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


class AlertaListaTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    @mock.patch.object(dao.AlertaMGPDAO, 'execute')
    def test_alert_list(self, _AlertaMGPDAO_execute):
        orgao_id = '0000000'
        alertas_return = [
            (
                0000,
                'mock',
                '2020-01-01',
                int(orgao_id),
                -1,
                'id_alrt',
                'PRCR',
                'desc1',
                'classe1',
                'ext1234',
                'alrtkey',
                # 0
            ),
            (
                0000,
                'mock',
                '2020-01-01',
                int(orgao_id),
                -1,
                'id_alrt',
                'PRCR',
                'desc1',
                'classe1',
                'ext1234',
                'alrtkey',
                # 1
            ),
        ]

        alertas_expected = [
            {
                'doc_dk': 0,
                'num_doc': 'mock',
                'data_alerta': '2020-01-01',
                'orgao': 0,
                'id_alerta': 'id_alrt',
                'dias_passados': -1,
                'sigla': 'PRCR',
                'descricao': 'desc1',
                'classe_hierarquia': 'classe1',
                'num_externo': 'ext1234',
                'alrt_key': 'alrtkey',
                # 'flag_dispensado': 0
            },
            {
                'doc_dk': 0,
                'num_doc': 'mock',
                'data_alerta': '2020-01-01',
                'orgao': 0,
                'id_alerta': 'id_alrt',
                'dias_passados': -1,
                'sigla': 'PRCR',
                'descricao': 'desc1',
                'classe_hierarquia': 'classe1',
                'num_externo': 'ext1234',
                'alrt_key': 'alrtkey',
                # 'flag_dispensado': 1
            }
        ]

        _AlertaMGPDAO_execute.return_value = alertas_return

        url = reverse(
            'dominio:lista_alertas',
            args=(orgao_id,)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, alertas_expected)

    @mock.patch.object(dao.AlertaMGPDAO, 'get')
    def test_alert_tipo(self, _AlertaMGPDAO_get):
        orgao_id = '0000000'
        tipo_alerta = 'ALRT'

        alertas_return = [
            {
                'sigla': 'mock',
                'doc_dk': 0000,
                'num_doc': 'mock',
                'data_alerta': '2020-01-01',
                'orgao': int(orgao_id),
                'id_alerta': 'id_alrt',
                'dias_passados': -1,
                'descricao': 'desc1',
                'classe_hierarquia': 'classe1',
                'num_externo': 'ext1234',
                'alrt_key': 'alrtkey',
                # 'flag_dispensado': 0
            },
        ]

        alertas_expected = [
            {
                'sigla': 'mock',
                'doc_dk': 0,
                'num_doc': 'mock',
                'data_alerta': '2020-01-01',
                'orgao': 0,
                'id_alerta': 'id_alrt',
                'dias_passados': -1,
                'descricao': 'desc1',
                'classe_hierarquia': 'classe1',
                'num_externo': 'ext1234',
                'alrt_key': 'alrtkey',
                # 'flag_dispensado': 0
            }
        ]

        _AlertaMGPDAO_get.return_value = alertas_return

        url = reverse(
            'dominio:lista_alertas',
            args=(orgao_id,)
        )
        resp = self.client.get(url, kwargs={'tipo_alerta': tipo_alerta})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, alertas_expected)


class AlertaResumoTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch.object(dao.AlertasDAO, "execute")
    def test_alert_resumo(self, _execute_resumo_dao):
        orgao_id = '12345'

        # _execute_compras_dao.return_value = [
        #     ("COMP", "mock 1", int(orgao_id), 10),
        #     ("COMP", "mock 2", int(orgao_id), 11),
        # ]
        # _execute_mgp_dao.return_value = [
        #     ("OUVI", "mock 3", int(orgao_id), 12),
        #     ("PRCR", "mock 4", int(orgao_id), 13),
        # ]

        _execute_resumo_dao.return_value = [
            ("COMP", 10),
            ("COMP", 11),
            ("OUVI", 12),
            ("PRCR", 13),
        ]

        alertas_expected = [
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
                'count': 11
            },
            {
                'sigla': 'OUVI',
                'count': 12,
            },
        ]

        url = reverse(
            'dominio:resumo_alertas',
            args=(orgao_id,)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, alertas_expected)


class AlertaComprasTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch.object(dao.AlertaComprasDAO, "execute")
    def test_alert_compras(self, _execute):
        return_alerta = [
            (
                'COMP',
                'Contrato 1',
                '98765',
                'Contrato ID 1',
                'ITEM 1',
                'alrtkey1',
                # 0
            ),
            (
                'COMP',
                'Contrato 2',
                '12345',
                'Contrato ID 2',
                'ITEM 2',
                'alrtkey2',
                # 0
            ),
        ]
        _execute.return_value = return_alerta
        orgao_id = '0000000'
        expected_output = [
            {
                'sigla': 'COMP',
                'contrato': 'Contrato 1',
                'iditem': 98765,
                'contrato_iditem': 'Contrato ID 1',
                'item': 'ITEM 1',
                'alrt_key': 'alrtkey1',
                # 'flag_dispensado': 0
            },
            {
                'sigla': 'COMP',
                'contrato': 'Contrato 2',
                'iditem': 12345,
                'contrato_iditem': 'Contrato ID 2',
                'item': 'ITEM 2',
                'alrt_key': 'alrtkey2',
                # 'flag_dispensado': 0

            }
        ]

        url = reverse(
            'dominio:compras_alertas',
            args=(orgao_id,)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_output)


class TestDispensarAlertas(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.orgao_id = "12345"
        self.alerta_id = "AAA.abc123.12345"
        self.url = reverse(
            "dominio:dispensar_alerta",
            args=(self.orgao_id, self.alerta_id),
        )

        self.dispensa_patcher = mock.patch(
            "dominio.alertas.views.DispensaAlertaController"
        )
        self.controller_obj_mock = mock.Mock()
        self.dispensa_controller_mock = self.dispensa_patcher.start()
        self.dispensa_controller_mock.return_value = self.controller_obj_mock

    def tearDown(self):
        super().tearDown()
        self.dispensa_patcher.stop()

    def test_post_dispensa_alerta(self):
        resp = self.client.post(self.url)

        self.dispensa_controller_mock.assert_called_once_with(
            self.orgao_id, self.alerta_id
        )
        self.controller_obj_mock.dispensa_para_orgao.assert_called_once_with()
        self.assertEqual(resp.status_code, 201)


class TestRetornaAlertas(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.orgao_id = "12345"
        self.alerta_id = "AAA.abc123.12345"
        self.url = reverse(
            "dominio:retornar_alerta",
            args=(self.orgao_id, self.alerta_id),
        )

        self.dispensa_patcher = mock.patch(
            "dominio.alertas.views.DispensaAlertaController"
        )
        self.controller_obj_mock = mock.Mock()
        self.dispensa_controller_mock = self.dispensa_patcher.start()
        self.dispensa_controller_mock.return_value = self.controller_obj_mock

    def tearDown(self):
        super().tearDown()
        self.dispensa_patcher.stop()

    def test_post_retorna_alerta(self):
        resp = self.client.post(self.url)

        self.dispensa_controller_mock.assert_called_once_with(
            self.orgao_id, self.alerta_id
        )
        self.controller_obj_mock.retorna_para_orgao.assert_called_once_with()
        self.assertEqual(resp.status_code, 200)


class AlertasOverlayTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    @mock.patch.object(dao.AlertasOverlayDAO, "get")
    def test_alert_overlay(self, _get):
        docu_dk = '12345'

        _get.return_value = [{'data': 1}]

        alertas_expected = [{'data': 1}]

        url = reverse(
            'dominio:overlay_alertas',
            args=(docu_dk,)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, alertas_expected)


class TestEnviarAlertasComprasOuvidoria(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.mock_jwt.return_value = {"cargo": settings.PROMOTOR_CARGO_SIGLA}

        self.orgao_id = "12345"
        self.alerta_sigla = "COMP"
        self.alerta_id = "abc12345"
        self.url = reverse(
            "dominio:alerta_ouvidoria",
            args=(self.orgao_id, self.alerta_sigla, self.alerta_id)
        )

        self.controller_patcher = mock.patch(
            "dominio.alertas.views.EnviaAlertaComprasOuvidoriaController"
        )
        self.controller_mock = self.controller_patcher.start()

        self.status = 201
        self.resp = {"detail": "alerta enviado com sucesso para ouvidoria"}
        self.controller_obj_mock = mock.Mock()
        self.controller_obj_mock.envia.return_value = (self.resp, self.status)
        self.controller_mock.return_value = self.controller_obj_mock

    def tearDown(self):
        super().tearDown()
        self.controller_patcher.stop()

    def test_envia_alerta_compras_para_ouvidoria(self):
        resp = self.client.post(self.url)

        self.controller_obj_mock.envia.assert_called_once_with()
        self.controller_mock.assert_called_once_with(
            self.orgao_id,
            self.alerta_id
        )
        self.assertEqual(resp.status_code, self.status)


class TestEnviarAlertasISPSOuvidoria(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.mock_jwt.return_value = {"cargo": settings.PROMOTOR_CARGO_SIGLA}

        self.orgao_id = "12345"
        self.alerta_sigla = "ISPS"
        self.alerta_id = "abc12345"

        self.url = reverse(
            "dominio:alerta_ouvidoria",
            args=(self.orgao_id, self.alerta_sigla, self.alerta_id)
        )

        self.controller_patcher = mock.patch(
            "dominio.alertas.views.EnviaAlertaISPSOuvidoriaController"
        )
        self.controller_mock = self.controller_patcher.start()

        self.status = 201
        self.resp = {"detail": "alerta enviado com sucesso para ouvidoria"}
        self.controller_obj_mock = mock.Mock()
        self.controller_obj_mock.envia.return_value = (self.resp, self.status)
        self.controller_mock.return_value = self.controller_obj_mock

    def tearDown(self):
        super().tearDown()
        self.controller_patcher.stop()

    def test_envia_alerta_compras_para_ouvidoria(self):
        resp = self.client.post(self.url)

        self.controller_obj_mock.envia.assert_called_once_with()
        self.controller_mock.assert_called_once_with(
            self.orgao_id,
            self.alerta_id
        )
        self.assertEqual(resp.status_code, self.status)

    def test_bad_request_alerta_sigla_invalida(self):
        alerta_sigla = "AAA"
        url = reverse(
            "dominio:alerta_ouvidoria",
            args=(self.orgao_id, alerta_sigla, self.alerta_id)
        )
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 400)


class TestBaixarAlertas(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.orgao_id = 10
        self.tipo_alerta = 'PRCR'
        self.url_mgp = (
            reverse("dominio:baixar_alertas", args=(self.orgao_id,)) +
            f'?tipo_alerta={self.tipo_alerta}'
        )
        self.url_notype = reverse(
            "dominio:baixar_alertas",
            args=(self.orgao_id,)
        )

        self.dao_mgp_exec_patcher = mock.patch(
            "dominio.alertas.dao.BaixarAlertasDAO.execute"
        )
        self.dao_mgp_exec_mock = self.dao_mgp_exec_patcher.start()
        self.dao_mgp_exec_mock.return_value = [
            ('mck', 0, 'nr1', 'mck', 10, 'id'),
            ('mck', 0, 'nr2', 'mck', 10, 'id'),
        ]

    def tearDown(self):
        super().tearDown()
        cache.clear()
        self.dao_mgp_exec_patcher.stop()

    def test_correct_response_mgp(self):
        resp = self.client.get(self.url_mgp)

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
                f'filename="Alerta-{self.tipo_alerta}-{date.today()}.xlsx"'
            )
        )

    def test_no_data(self):
        self.dao_mgp_exec_mock.return_value = []
        resp = self.client.get(self.url_mgp)

        self.assertEqual(resp.status_code, 404)

    def test_no_alert_type(self):
        resp = self.client.get(self.url_notype)
        self.assertEqual(resp.status_code, 404)
