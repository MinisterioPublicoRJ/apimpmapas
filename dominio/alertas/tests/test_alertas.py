from datetime import datetime
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from dominio.alertas import dao
from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


class AlertaListaTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    @mock.patch('dominio.alertas.views.Alerta')
    def test_alert_list(self, _Alerta):
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
                'classe_hier': 'mock',
                'dias_passados': -1
            }
        ]

        _Alerta.validos_por_orgao.return_value = alertas_return

        url = reverse(
            'dominio:lista_alertas',
            args=(orgao_id,)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, alertas_expected)

    @mock.patch('dominio.alertas.views.Alerta')
    def test_alert_tipo(self, _Alerta):
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
                'classe_hier': 'mock',
                'dias_passados': -1
            }
        ]

        _Alerta.validos_por_orgao.return_value = alertas_return

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


class AlertaComprasTest(NoJWTTestCase, NoCacheTestCase, TestCase):

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

        self.get_hbase_table_patcher = mock.patch(
            "dominio.alertas.views.get_hbase_table"
        )
        self.get_hbase_table_mock = self.get_hbase_table_patcher.start()
        self.hbase_obj_mock = mock.Mock()
        self.get_hbase_table_mock.return_value = self.hbase_obj_mock

        self.orgao_id = "12345"
        self.sigla_alerta = "comp"
        self.url = reverse(
            "dominio:dispensar_alerta",
            args=(self.orgao_id, self.sigla_alerta),
        )

    def tearDown(self):
        super().tearDown()
        self.get_hbase_table_patcher.stop()

    def test_post_dispensa_alerta_compra(self):
        alerta_id = "abc123"
        self.url += f"?alerta_id={alerta_id}"
        resp = self.client.post(self.url)

        self.get_hbase_table_mock.assert_called_once_with(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            settings.HBASE_DISPENSAR_ALERTAS_TABLE,
        )
        expected_hbase_key = (
            f"{self.orgao_id}_{self.sigla_alerta}_{alerta_id}".encode()
        )
        expected_hbase_data = {
            b"dados_alertas:orgao": self.orgao_id.encode(),
            b"dados_alertas:sigla": self.sigla_alerta.encode(),
            b"dados_alertas:alerta_id": alerta_id.encode(),
        }
        self.hbase_obj_mock.put.assert_called_once_with(
                expected_hbase_key,
                expected_hbase_data
        )
        self.assertEqual(resp.status_code, 200)
