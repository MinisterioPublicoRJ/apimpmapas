from datetime import datetime
from unittest import mock

from django.test import TestCase
from django.urls import reverse

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

    @mock.patch('dominio.alertas.views.Alerta')
    def test_alert_resumo(self, _Alerta):
        orgao_id = '0000000'

        alertas_return = [
            {
                'sigla': 'mock',
                'descricao': 'mock',
                'orgao': int(orgao_id),
                'count': 10
            },
        ]

        alertas_expected = [
            {
                'sigla': 'mock',
                'descricao': 'mock',
                'orgao': 0,
                'count': 10
            }
        ]

        _Alerta.resumo_por_orgao.return_value = alertas_return

        url = reverse(
            'dominio:resumo_alertas',
            args=(orgao_id,)
        )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, alertas_expected)


class AlertaComprasTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    def test_alert_compras(self):
        orgao_id = '0000000'

        expected_output = [
            {
                'sigla': 'COMP',
                'contrato': '2020001923',
                'iditem': 58818,
                'contrato_iditem': '2020001923-58818',
                'item': (
                    'MASCARA CIRURGICA DESCARTAVEL - MATERIAL MASCARA: T'
                    'ECIDO NAO TECIDO, QUANTIDADE CAMADA: 3, CLIP NASAL: METAL'
                    'ICO, FORMATO: SIMPLES (RETANGULAR), MATERIAL VISOR: N/A, '
                    'GRAMATURA: 30 G/MÃ‚Â², FILTRO: N/D, FIXACAO: AMARRAS, COR'
                    ': N/D')
            },
            {
                'sigla': 'COMP',
                'contrato': '2020101010',
                'iditem': 12345,
                'contrato_iditem': '2020101010-12345',
                'item': 'LUVA COMESTIVEL DE TESTE'

            }
        ]

        url = reverse(
            'dominio:compras_alertas',
            args=(orgao_id,)
        )
        resp = self.client.get(url)
        print(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_output)
