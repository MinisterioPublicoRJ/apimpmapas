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

        expected_query = (
                "SELECT acervo "
                "FROM exadata_aux.tb_acervo "
                "WHERE cod_orgao = 0 "
                "AND tipo_acervo = 1 "
                "AND dt_inclusao = to_timestamp('2', 'yyyy-MM-dd')")

        _execute.assert_called_once_with(expected_query)

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
            args=('0', '1', '2')))

        expected_response = {
            'acervo_fim': 100,
            'acervo_inicio': 100,
            'variacao': 0.0
        }

        expected_query = """
                SELECT 
                    acervo_fim,
                    acervo_inicio,
                    (acervo_fim - acervo_inicio)/acervo_inicio as variacao
                FROM (
                    SELECT
                        SUM(tb_data_fim.acervo) as acervo_fim,
                        SUM(tb_data_inicio.acervo_inicio) as acervo_inicio
                        FROM exadata_aux.tb_acervo tb_data_fim
                    INNER JOIN (
                        SELECT
                            acervo as acervo_inicio,
                            dt_inclusao as data_inicio,
                            cod_orgao,
                            tipo_acervo
                        FROM exadata_aux.tb_acervo
                        WHERE dt_inclusao = to_timestamp(
                            '1', 'yyyy-MM-dd')
                        ) tb_data_inicio
                    ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                        AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                    INNER JOIN exadata_aux.tb_regra_negocio_investigacao regras
                    ON regras.cod_atribuicao = tb_data_fim.cod_atribuicao
                        AND regras.classe_documento = tb_data_fim.tipo_acervo
                    WHERE tb_data_fim.dt_inclusao = to_timestamp(
                        '2', 'yyyy-MM-dd')
                    AND tb_data_fim.cod_orgao = 0) t
                """

        _execute.assert_called_once_with(expected_query)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_acervo_variation_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse(
            'dominio:acervo_variation',
            args=('0', '1', '2')))

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

        expected_query = """
                SELECT
                    tb_data_fim.acervo as acervo_fim,
                    tb_data_inicio.acervo_inicio,
                    (acervo - acervo_inicio)/acervo_inicio as variacao,
                    tb_data_fim.cod_orgao as cod_orgao
                FROM exadata_aux.tb_acervo tb_data_fim
                INNER JOIN (
                    SELECT
                        acervo as acervo_inicio,
                        dt_inclusao as data_inicio,
                        cod_orgao,
                        tipo_acervo
                    FROM exadata_aux.tb_acervo
                    WHERE dt_inclusao = to_timestamp(
                        '1', 'yyyy-MM-dd')
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                WHERE tb_data_fim.dt_inclusao = to_timestamp(
                    '2', 'yyyy-MM-dd')
                AND tb_data_fim.tipo_acervo = 0
                ORDER BY variacao DESC
                LIMIT 3;
                """

        _execute.assert_called_once_with(expected_query)

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
            ('20', '100', '1000', '500', '300', '450', '700',
             '400', '50', '950')]
        response = self.client.get(reverse(
            'dominio:outliers',
            args=('0', '1')))

        expected_response = {
            'cod_atribuicao': 20,
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
                SELECT B.cod_atribuicao,
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
                ON A.cod_atribuicao = B.cod_atribuicao
                AND A.dt_inclusao = B.dt_inclusao
                WHERE A.cod_orgao = 0
                AND B.dt_inclusao = to_timestamp('1', 'yyyy-MM-dd')
                """

        _execute.assert_called_once_with(expected_query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_outliers_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse(
            'dominio:outliers',
            args=('0', '1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class SaidasViewTest(TestCase):

    @mock.patch('dominio.views.execute')
    def test_saidas_result(self, _execute):
        _execute.return_value = [
            ('0', '100', '25', '0.7', '2020-02-06 17:19:08.952040000')]
        response = self.client.get(reverse(
            'dominio:saidas',
            args=('100',)))

        expected_response = {
            'saidas': 0,
            'id_orgao': 100,
            'cod_pct': 25,
            'percent_rank': 0.7,
            'dt_calculo': '2020-02-06 17:19:08.952040000'
        }

        expected_query = """
                SELECT saidas, id_orgao, cod_pct, percent_rank, dt_calculo
                FROM exadata_aux.tb_saida
                WHERE id_orgao = 100
                """

        _execute.assert_called_once_with(expected_query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.execute')
    def test_saidas_no_result(self, _execute):
        _execute.return_value = []
        response = self.client.get(reverse(
            'dominio:saidas',
            args=('1',)))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)
