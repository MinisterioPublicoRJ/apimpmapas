from datetime import datetime
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from dominio.alertas import controllers, dao
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
                'descricao': 'mock',
                'doc_dk': 0000,
                'num_doc': 'mock',
                'num_ext': 'mock',
                'etiqueta': 'mock',
                'classe_doc': 'mock',
                'data_alerta': datetime(2020, 1, 1),
                'orgao': int(orgao_id),
                'id_alerta': 'id_alrt',
                'classe_hier': 'mock',
                'dias_passados': -1
            },
        ]

        alertas_expected = [
            {
                'sigla': 'mock',
                'descricao': 'mock',
                'doc_dk': 0,
                'num_doc': 'mock',
                'num_ext': 'mock',
                'etiqueta': 'mock',
                'classe_doc': 'mock',
                'data_alerta': '2020-01-01T00:00:00Z',
                'orgao': 0,
                'id_alerta': 'id_alrt',
                'classe_hier': 'mock',
                'dias_passados': -1
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
                'descricao': 'mock',
                'doc_dk': 0000,
                'num_doc': 'mock',
                'num_ext': 'mock',
                'etiqueta': 'mock',
                'classe_doc': 'mock',
                'data_alerta': datetime(2020, 1, 1),
                'orgao': int(orgao_id),
                'id_alerta': 'id_alrt',
                'classe_hier': 'mock',
                'dias_passados': -1
            },
        ]

        alertas_expected = [
            {
                'sigla': 'mock',
                'descricao': 'mock',
                'doc_dk': 0,
                'num_doc': 'mock',
                'num_ext': 'mock',
                'etiqueta': 'mock',
                'classe_doc': 'mock',
                'data_alerta': '2020-01-01T00:00:00Z',
                'orgao': 0,
                'id_alerta': 'id_alrt',
                'classe_hier': 'mock',
                'dias_passados': -1
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

    @mock.patch.object(dao.ResumoAlertasMGPDAO, "execute")
    @mock.patch.object(dao.ResumoAlertasComprasDAO, "execute")
    def test_alert_resumo(self, _execute_compras_dao, _execute_mgp_dao):
        orgao_id = '12345'

        _execute_compras_dao.return_value = [
            ("COMP", "mock 1", int(orgao_id), 10),
            ("COMP", "mock 2", int(orgao_id), 11),
        ]
        _execute_mgp_dao.return_value = [
            ("OUVI", "mock 3", int(orgao_id), 12),
            ("PRCR", "mock 4", int(orgao_id), 13),
        ]

        alertas_expected = [
            {
                'sigla': 'PRCR',
                'descricao': 'mock 4',
                'orgao': 12345,
                'count': 13,
            },
            {
                'sigla': 'COMP',
                'descricao': 'mock 1',
                'orgao': 12345,
                'count': 10,
            },
            {
                'sigla': 'COMP',
                'descricao': 'mock 2',
                'orgao': 12345,
                'count': 11
            },
            {
                'sigla': 'OUVI',
                'descricao': 'mock 3',
                'orgao': 12345,
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

        self.dispensa_patcher = mock.patch.object(
            controllers.DispensaAlertaComprasController, "dispensa_para_orgao"
        )
        self.dispensa_controller_mock = self.dispensa_patcher.start()

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

        self.dispensa_patcher = mock.patch.object(
            controllers.DispensaAlertaComprasController, "retorna_para_orgao"
        )
        self.dispensa_controller_mock = self.dispensa_patcher.start()

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
        self.assertEqual(resp.status_code, 200)

    def test_bad_request_missing_alerta_id(self):
        resp = self.client.post(self.url)

        self.assertEqual(resp.status_code, 400)


class TestEnviarAlertasComprasOuvidoria(NoJWTTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.orgao_id = "12345"
        self.url = reverse(
            "dominio:alerta_compras_ouvidoria",
            args=(self.orgao_id,)
        )

        self.controller_patcher = mock.patch(
            "dominio.alertas.views.controllers"
            ".EnviaAlertaComprasOuvidoriaController"
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
