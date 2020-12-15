from datetime import datetime, date
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache

from dominio.alertas import dao
from dominio.alertas.tests.testconf import (
    RemoveFiltroAlertasDispensadosTestCase,
)
from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


class AlertaListaTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    @mock.patch.object(dao.AlertaMGPDAO, 'get')
    def test_alert_list(self, _AlertaMGPDAO_get):
        orgao_id = '0000000'
        alertas_return = [
            {
                'sigla': 'mock',
                'doc_dk': 0000,
                'num_doc': 'mock',
                'data_alerta': datetime(2020, 1, 1),
                'orgao': int(orgao_id),
                'id_alerta': 'id_alrt',
                'dias_passados': -1,
                'descricao': 'desc1',
                'classe_hierarquia': 'classe1',
                'num_externo': 'ext1234'
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
                'num_externo': 'ext1234'
            }
        ]

        _AlertaMGPDAO_get.return_value = alertas_return

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
                'data_alerta': datetime(2020, 1, 1),
                'orgao': int(orgao_id),
                'id_alerta': 'id_alrt',
                'dias_passados': -1,
                'descricao': 'desc1',
                'classe_hierarquia': 'classe1',
                'num_externo': 'ext1234'
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
                'num_externo': 'ext1234'
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
    @mock.patch.object(dao.AlertaMaxPartitionDAO, "execute")
    @mock.patch.object(dao.AlertasDAO, "execute")
    def test_alert_resumo(self, _execute_resumo_dao, _execute_max_dt):
        orgao_id = '12345'

        # _execute_compras_dao.return_value = [
        #     ("COMP", "mock 1", int(orgao_id), 10),
        #     ("COMP", "mock 2", int(orgao_id), 11),
        # ]
        # _execute_mgp_dao.return_value = [
        #     ("OUVI", "mock 3", int(orgao_id), 12),
        #     ("PRCR", "mock 4", int(orgao_id), 13),
        # ]
        _execute_max_dt.return_value = [('20201010',)]

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


class AlertaComprasTest(
        RemoveFiltroAlertasDispensadosTestCase,
        NoJWTTestCase,
        NoCacheTestCase,
        TestCase):

    @mock.patch.object(dao.AlertaComprasDAO, "execute")
    def test_alert_compras(self, _execute):
        return_alerta = [
            ('COMP', 'Contrato 1', '98765', 'Contrato ID 1', 'ITEM 1'),
            ('COMP', 'Contrato 2', '12345', 'Contrato ID 2', 'ITEM 2'),
        ]
        _execute.return_value = return_alerta
        orgao_id = '0000000'
        expected_output = [
            {
                'sigla': 'COMP',
                'contrato': 'Contrato 1',
                'iditem': 98765,
                'contrato_iditem': 'Contrato ID 1',
                'item': 'ITEM 1'
            },
            {
                'sigla': 'COMP',
                'contrato': 'Contrato 2',
                'iditem': 12345,
                'contrato_iditem': 'Contrato ID 2',
                'item': 'ITEM 2'

            }
        ]

        url = reverse(
            'dominio:compras_alertas',
            args=(orgao_id,)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_output)


class TestDispensarAlertasCompras(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.orgao_id = "12345"
        self.url = reverse(
            "dominio:dispensar_alerta",
            args=(self.orgao_id,),
        )

        self.dispensa_patcher = mock.patch(
            "dominio.alertas.views.DispensaAlertaComprasController"
        )
        self.controller_obj_mock = mock.Mock()
        self.dispensa_controller_mock = self.dispensa_patcher.start()
        self.dispensa_controller_mock.return_value = self.controller_obj_mock

    def tearDown(self):
        super().tearDown()
        self.dispensa_patcher.stop()

    def test_post_dispensa_alerta_compra(self):
        alerta_id = "abc123"
        self.url += f"?alerta_id={alerta_id}"
        resp = self.client.post(self.url)

        self.dispensa_controller_mock.assert_called_once_with(
            self.orgao_id, alerta_id
        )
        self.controller_obj_mock.dispensa_para_orgao.assert_called_once_with()
        self.assertEqual(resp.status_code, 201)

    def test_bad_request_missing_alerta_id(self):
        resp = self.client.post(self.url)

        self.assertEqual(resp.status_code, 400)


class TestRetornaAlertasCompras(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.orgao_id = "12345"
        self.url = reverse(
            "dominio:retornar_alerta",
            args=(self.orgao_id,),
        )

        self.dispensa_patcher = mock.patch(
            "dominio.alertas.views.DispensaAlertaComprasController"
        )
        self.controller_obj_mock = mock.Mock()
        self.dispensa_controller_mock = self.dispensa_patcher.start()
        self.dispensa_controller_mock.return_value = self.controller_obj_mock

    def tearDown(self):
        super().tearDown()
        self.dispensa_patcher.stop()

    def test_post_retorna_alerta_compra(self):
        alerta_id = "abc123"
        self.url += f"?alerta_id={alerta_id}"
        resp = self.client.post(self.url)

        self.dispensa_controller_mock.assert_called_once_with(
            self.orgao_id, alerta_id
        )
        self.controller_obj_mock.retorna_para_orgao.assert_called_once_with()
        self.assertEqual(resp.status_code, 200)

    def test_bad_request_missing_alerta_id(self):
        resp = self.client.post(self.url)

        self.assertEqual(resp.status_code, 400)


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
        self.orgao_id = "12345"
        self.alerta_sigla = "COMP"
        self.url = reverse(
            "dominio:alerta_ouvidoria",
            args=(self.orgao_id, self.alerta_sigla)
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
        alerta_id = "abc12345"
        self.url += f"?alerta_id={alerta_id}"
        resp = self.client.post(self.url)

        self.controller_obj_mock.envia.assert_called_once_with()
        self.controller_mock.assert_called_once_with(self.orgao_id, alerta_id)
        self.assertEqual(resp.status_code, self.status)

    def test_bad_request_alerta_id_nao_informado(self):
        resp = self.client.post(self.url)

        self.assertEqual(resp.status_code, 400)


class TestEnviarAlertasISPSOuvidoria(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.orgao_id = "12345"
        self.alerta_sigla = "ISPS"
        self.alerta_id = "abc12345"

        self.url = reverse(
            "dominio:alerta_ouvidoria",
            args=(self.orgao_id, self.alerta_sigla)
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
        self.url += f"?alerta_id={self.alerta_id}"
        resp = self.client.post(self.url)

        self.controller_obj_mock.envia.assert_called_once_with()
        self.controller_mock.assert_called_once_with(
            self.orgao_id,
            self.alerta_id
        )
        self.assertEqual(resp.status_code, self.status)

    def test_bad_request_alerta_id_nao_informado(self):
        resp = self.client.post(self.url)

        self.assertEqual(resp.status_code, 400)

    def test_bad_request_alerta_sigla_invalida(self):
        url = reverse("dominio:alerta_ouvidoria", args=(self.orgao_id, "AAA"))
        url += f"?alerta_id={self.alerta_id}"
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 400)


class TestBaixarAlertas(
        RemoveFiltroAlertasDispensadosTestCase,
        NoJWTTestCase,
        TestCase
):
    def setUp(self):
        super().setUp()
        self.orgao_id = 10
        self.url_comp = (
            reverse("dominio:baixar_alertas", args=(self.orgao_id,)) +
            '?tipo_alerta=COMP'
        )
        self.tipo_alerta_mgp = 'PRCR'
        self.url_mgp = (
            reverse("dominio:baixar_alertas", args=(self.orgao_id,)) +
            f'?tipo_alerta={self.tipo_alerta_mgp}'
        )
        self.url_notype = reverse(
            "dominio:baixar_alertas",
            args=(self.orgao_id,)
        )

        self.dao_mgp_exec_patcher = mock.patch(
            "dominio.alertas.dao.AlertaMGPDAO.execute"
        )
        self.dao_mgp_exec_mock = self.dao_mgp_exec_patcher.start()
        self.dao_mgp_exec_mock.return_value = [
            ('mck', 0, 'nr1', 'mck', 10, 'id', -1, 'dsc1', 'cls1', 'ext1'),
            ('mck', 0, 'nr2', 'mck', 10, 'id', -1, 'dsc2', 'cls2', 'ext2'),
        ]

        self.dao_comp_exec_patcher = mock.patch(
            "dominio.alertas.dao.AlertaComprasDAO.execute"
        )
        self.dao_comp_exec_mock = self.dao_comp_exec_patcher.start()
        self.dao_comp_exec_mock.return_value = [
            ('COMP', 'Contrato 1', '98765', 'Contrato ID 1', 'ITEM 1'),
            ('COMP', 'Contrato 1', '98765', 'Contrato ID 1', 'ITEM 1')
        ]

        self.dao_alerta_max_part_patcher = mock.patch(
            "dominio.alertas.dao.AlertaMaxPartitionDAO.execute"
        )
        self.dao_alerta_max_part_mock =\
            self.dao_alerta_max_part_patcher.start()
        self.dao_alerta_max_part_mock.return_value = (("2020-1-1",),)

    def tearDown(self):
        super().tearDown()
        cache.clear()
        self.dao_mgp_exec_patcher.stop()
        self.dao_comp_exec_patcher.stop()
        self.dao_alerta_max_part_patcher.stop()

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
                f'filename="Alerta-{self.tipo_alerta_mgp}-{date.today()}.xlsx"'
            )
        )

    def test_correct_response_comp(self):
        resp = self.client.get(self.url_comp)

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
                f'filename="Alerta-COMP-{date.today()}.xlsx"'
            )
        )

    def test_no_alert_type(self):
        resp = self.client.get(self.url_notype)
        self.assertEqual(resp.status_code, 404)
