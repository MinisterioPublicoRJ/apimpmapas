from datetime import datetime
from unittest import mock

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
