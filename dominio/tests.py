from unittest import mock

from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class AcervoViewTest(TestCase):

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_result(self, _execute):
        _execute.return_value = [('10',)]
        response = self.client.get(reverse('dominio:acervo', args=('0', '1', '2')))

        expected_response = {'acervo_qtd': 10}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse('dominio:acervo', args=('0', '1', '2')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class AcervoVariationViewTest(TestCase):

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_result(self, _execute):
        _execute.return_value = [('100', '100', '0.0')]
        response = self.client.get(reverse('dominio:acervo_variation', args=('0', '1', '2', '3')))

        expected_response = {'acervo_fim': 100, 'acervo_inicio': 100, 'variacao': 0.0}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse('dominio:acervo_variation', args=('0', '1', '2', '3')))

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
        response = self.client.get(reverse('dominio:acervo_variation_topn', args=('0', '1', '2', '3')))

        expected_response = [
            {'acervo_fim': 100, 'acervo_inicio': 50, 'variacao': 100.0, 'cod_orgao': 1},
            {'acervo_fim': 50, 'acervo_inicio': 100, 'variacao': -50.0, 'cod_orgao': 2},
            {'acervo_fim': 300, 'acervo_inicio': 100, 'variacao': 200.0, 'cod_orgao': 3}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse('dominio:acervo_variation_topn', args=('0', '1', '2', '3')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)

