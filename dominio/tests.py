from unittest import mock

from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class AcervoViewTest(TestCase):

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_result(self, _execute):
        _execute.return_value = [('10',)]
        response = self.client.get(reverse(
            'dominio:acervo',
            args=('0', '1', '2')))

        expected_response = {'acervo_qtd': 10}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse(
            'dominio:acervo',
            args=('0', '1', '2')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class AcervoVariationViewTest(TestCase):

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_result(self, _execute):
        _execute.return_value = [('100', '100', '0.0')]
        response = self.client.get(reverse(
            'dominio:acervo_variation',
            args=('0', '1', '2', '3')))

        expected_response = {
            'acervo_fim': 100,
            'acervo_inicio': 100,
            'variacao': 0.0
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse(
            'dominio:acervo_variation',
            args=('0', '1', '2', '3')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class AcervoVariationTopNViewTest(TestCase):

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_result(self, _execute):
        _execute.return_value = [
            ('100', '50', '100.0', 1),
            ('50', '100', '-50.0', 2),
            ('300', '100', '200.0', 3)
        ]
        response = self.client.get(reverse(
            'dominio:acervo_variation_topn',
            args=('0', '1', '2', '3')))

        expected_response = [
            {
                'acervo_fim': 100,
                'acervo_inicio': 50,
                'variacao': 100.0,
                'cod_orgao': 1
            },
            {
                'acervo_fim': 50,
                'acervo_inicio': 100,
                'variacao': -50.0,
                'cod_orgao': 2
            },
            {
                'acervo_fim': 300,
                'acervo_inicio': 100,
                'variacao': 200.0,
                'cod_orgao': 3
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse(
            'dominio:acervo_variation_topn',
            args=('0', '1', '2', '3')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class OutliersViewTest(TestCase):

    @mock.patch('dominio.views.execute')
    def test_outliers_result(self, _execute):
        _execute.return_value = [
            ('TC de Tal Coisa', '100', '1000', '500', '300', '450', '700',
             '400', '50', '950')]
        response = self.client.get(reverse(
            'dominio:outliers',
            args=('0', '1', '2')))

        expected_response = {
            'pacote_atribuicao': 'TC de Tal Coisa',
            'minimo': 100,
            'maximo': 1000,
            'media': 500,
            'primeiro_quartil': 300,
            'mediana': 450,
            'terceiro_quartil': 700,
            'iqr': 400,
            'lout': 50,
            'hout': 950
        }

        expected_query = """
                SELECT B.pacote_atribuicao,
                B.minimo,
                B.maximo,
                B.media,
                B.primeiro_quartil,
                B.mediana,
                B.terceiro_quartil,
                B.iqr,
                B.lout,
                B.hout
                FROM exadata_aux.tb_acervo A
                INNER JOIN exadata_aux.tb_distribuicao B
                ON A.pacote_atribuicao = B.pacote_atribuicao
                AND A.dt_inclusao = B.dt_inclusao
                WHERE A.cod_orgao = 0
                AND A.tipo_acervo = 1
                AND B.dt_inclusao = to_timestamp('2', 'yyyy-MM-dd')
                """

        _execute.assert_called_once_with(expected_query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_outliers_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse(
            'dominio:outliers',
            args=('0', '1', '2')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)
