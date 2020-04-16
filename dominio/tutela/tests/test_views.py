from datetime import datetime, timedelta
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from dominio.tutela.views import DetalheProcessosJuizoView

from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


# Create your tests here.
class DetalheAcervoViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    @mock.patch('dominio.tutela.views.run_query')
    def test_acervo_variation_result(self, _run_query):
        _run_query.return_value = [
            (0, 'PROMO0', '30', '60', '-60.0'),
            (1, 'PROMO1', '100', '50', '100.0'),
            (2, 'PROMO2', '50', '100', '-50.0'),
            (3, 'PROMO3', '300', '100', '200.0')
        ]
        response = self.client.get(reverse(
            'dominio:suamesa-detalhe-investigacoes',
            args=('0')))

        expected_response = {
            "variacao_acervo": -60.0,
            "top_n": [
                {
                    'nm_promotoria': 'Promo3',
                    'variacao_acervo': 200.0,
                },
                {
                    'nm_promotoria': 'Promo1',
                    'variacao_acervo': 100.0,
                },
                {
                    'nm_promotoria': 'Promo2',
                    'variacao_acervo': -50.0,
                }
            ]
        }

        expected_query = """
                WITH tb_acervo_orgao_pct as (
                    SELECT *
                    FROM {namespace}.tb_acervo ac
                    INNER JOIN (
                        SELECT cod_pct
                        FROM {namespace}.atualizacao_pj_pacote
                        WHERE id_orgao = :orgao_id
                        ) org
                    ON org.cod_pct = ac.cod_atribuicao)
                SELECT
                    tb_data_fim.cod_orgao,
                    pc.orgi_nm_orgao as nm_orgao,
                    tb_data_fim.acervo_fim,
                    tb_data_inicio.acervo_inicio,
                    (acervo_fim - acervo_inicio)/acervo_inicio as variacao
                FROM (
                    SELECT cod_orgao, SUM(acervo) as acervo_fim
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_fim, 'yyyy-MM-dd')
                    GROUP BY cod_orgao
                    ) tb_data_fim
                INNER JOIN (
                    SELECT cod_orgao, SUM(acervo) as acervo_inicio
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_inicio, 'yyyy-MM-dd')
                    GROUP BY cod_orgao
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                INNER JOIN {namespace}.atualizacao_pj_pacote pc
                ON pc.id_orgao = tb_data_fim.cod_orgao
                """.format(namespace=settings.TABLE_NAMESPACE)

        dt_inicio = str(datetime.now().date() - timedelta(30))
        expected_parameters = {
            'orgao_id': 0,
            'dt_inicio': dt_inicio,
            'dt_fim': str(datetime.now().date())
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.tutela.views.run_query')
    def test_acervo_variation_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:suamesa-detalhe-investigacoes',
            args=('0')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class OutliersViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.tutela.views.run_query')
    def test_outliers_result(self, _run_query):
        _run_query.return_value = [
            ('0', '10', '20', '100', '1000', '500', '300',
             '450', '700', '400', '50', '950', '2020-03-20 00:00:00')
        ]
        response = self.client.get(reverse(
            'dominio:outliers',
            args=('0')))

        expected_response = {
            'cod_orgao': 0,
            'acervo_qtd': 10,
            'cod_atribuicao': 20,
            'minimo': 100,
            'maximo': 1000,
            'media': 500,
            'primeiro_quartil': 300,
            'mediana': 450,
            'terceiro_quartil': 700,
            'iqr': 400,
            'lout': 50,
            'hout': 950,
            'dt_inclusao': '2020-03-20 00:00:00'
        }

        expected_query = """
                SELECT
                cod_orgao,
                acervo,
                cod_atribuicao,
                minimo,
                maximo,
                media,
                primeiro_quartil,
                mediana,
                terceiro_quartil,
                iqr,
                lout,
                hout,
                dt_inclusao
                FROM {namespace}.tb_distribuicao
                WHERE cod_orgao = :orgao_id
                """.format(namespace=settings.TABLE_NAMESPACE)
        expected_parameters = {
            'orgao_id': 0
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.tutela.views.run_query')
    def test_outliers_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:outliers',
            args=('0')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class SaidasViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.tutela.views.run_query')
    def test_saidas_result(self, _run_query):
        _run_query.return_value = \
            [
                ('0', '100', '25', '0.7', '2020-02-06 17:19:08.952040000'),
            ]
        response = self.client.get(reverse(
            'dominio:saidas',
            args=('120',)))

        expected_response = {
            'saidas': 0,
            'id_orgao': 100,
            'cod_pct': 25,
            'percent_rank': 0.7,
            'dt_calculo': '2020-02-06 17:19:08.952040000'
        }

        expected_query = """
                SELECT saidas, id_orgao, cod_pct, percent_rank, dt_calculo
                FROM {namespace}.tb_saida
                WHERE id_orgao = :orgao_id
                """.format(namespace=settings.TABLE_NAMESPACE)
        expected_parameters = {'orgao_id': 120}

        _run_query.assert_called_once_with(expected_query, expected_parameters)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.tutela.views.run_query')
    def test_saidas_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:saidas',
            args=('120',)))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class EntradasViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.tutela.views.run_query')
    def test_entradas_result(self, _run_query):
        _run_query.return_value = \
            [
                (
                    '5', '0', '10', '4.2', '0.0',
                    '3.0', '5.0', '2.0', '1.0', '5.0'
                ),
            ]
        response = self.client.get(reverse(
            'dominio:entradas',
            args=('1', '2')))

        expected_response = {
            'nr_entradas_hoje': 5,
            'minimo': 0,
            'maximo': 10,
            'media': 4.2,
            'primeiro_quartil': 0.0,
            'mediana': 3.0,
            'terceiro_quartil': 5.0,
            'iqr': 2.0,
            'lout': 1.0,
            'hout': 5.0
        }

        expected_query = """
                SELECT
                    nr_entradas_hoje,
                    minimo,
                    maximo,
                    media,
                    primeiro_quartil,
                    mediana,
                    terceiro_quartil,
                    iqr,
                    lout,
                    hout
                FROM {namespace}.tb_dist_entradas
                WHERE comb_orga_dk = :orgao_id
                AND comb_cpf = :nr_cpf
                """.format(namespace=settings.TABLE_NAMESPACE)
        expected_parameters = {
            'orgao_id': 1,
            'nr_cpf': '2'
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.tutela.views.run_query')
    def test_entradas_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:entradas',
            args=('1', '2')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class DetalheProcessosJuizoViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    @mock.patch('dominio.tutela.views.run_query')
    def test_get_numero_acoes_propostas_pacote_atribuicao(self, _run_query):
        DetalheProcessosJuizoView\
            .get_numero_acoes_propostas_pacote_atribuicao(1)

        expected_query = """
            SELECT
                orgao_id,
                nm_orgao,
                nr_acoes_ultimos_60_dias,
                variacao_12_meses,
                nr_acoes_ultimos_30_dias
            FROM {namespace}.tb_detalhe_processo t1
            JOIN (
                SELECT cod_pct
                FROM {namespace}.tb_detalhe_processo
                WHERE orgao_id = :orgao_id) t2
              ON t1.cod_pct = t2.cod_pct
        """.format(namespace=settings.TABLE_NAMESPACE)
        expected_parameters = {
            "orgao_id": 1
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)

    @mock.patch('dominio.tutela.views.run_query')
    def test_detalhe_processos_result(self, _run_query):
        _run_query.side_effect = \
            [
                [(1, 'TC 1', 20, 1.0, 50),
                 (2, 'TC 2', 30, 0.5, 10),
                 (3, 'TC 3', 40, 0.75, 40),
                 (4, 'TC 4', 10, 0.75, 100),
                 (5, 'TC 5', 40, 0.75, 30)]
            ]
        response = self.client.get(reverse(
            'dominio:suamesa-detalhe-processos',
            args=('1')))

        expected_response = {
            'nr_acoes_propostas_60_dias': 20,
            'variacao_12_meses': 1.0,
            'top_n': [
                {'nm_promotoria': 'tc 4', 'nr_acoes_propostas_30_dias': 100},
                {'nm_promotoria': 'tc 1', 'nr_acoes_propostas_30_dias': 50},
                {'nm_promotoria': 'tc 3', 'nr_acoes_propostas_30_dias': 40}]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.tutela.views.run_query')
    def test_detalhe_processos_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:suamesa-detalhe-processos',
            args=('1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class ListaProcessosViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    # TODO: override settings
    @mock.patch('dominio.tutela.views.ListaProcessosView.PROCESSOS_SIZE')
    @mock.patch('dominio.tutela.views.run_query')
    def test_lista_processos_result(self, _run_query, _PROCESSOS_SIZE):
        _PROCESSOS_SIZE.return_value = 1

        _run_query.return_value = \
            [
                (
                    '1', 'Ação1', '200', '300', None,
                    'Personagens1', '2019-01-01 00:00:00',
                    'Andamento1', 'Link1'
                ),
                (
                    '1', 'Ação2', '200', '300', None,
                    'Personagens2', '2019-01-01 00:00:00',
                    'Andamento2', 'Link2'
                ),
            ]
        response_1 = self.client.get(reverse(
            'dominio:lista-processos',
            args=('1')) + '?page=1')
        response_2 = self.client.get(reverse(
            'dominio:lista-processos',
            args=('1')) + '?page=2')

        expected_response_page_1 = [
            {
                'id_orgao': '1',
                'classe_documento': 'Ação1',
                'docu_nr_mp': '200',
                'docu_nr_externo': '300',
                'docu_etiqueta': None,
                'docu_personagens': 'Personagens1',
                'dt_ultimo_andamento': '2019-01-01 00:00:00',
                'ultimo_andamento': 'Andamento1',
                'url_tjrj': 'Link1'
            }
        ]
        expected_response_page_2 = [
            {
                'id_orgao': '1',
                'classe_documento': 'Ação2',
                'docu_nr_mp': '200',
                'docu_nr_externo': '300',
                'docu_etiqueta': None,
                'docu_personagens': 'Personagens2',
                'dt_ultimo_andamento': '2019-01-01 00:00:00',
                'ultimo_andamento': 'Andamento2',
                'url_tjrj': 'Link2'
            }
        ]

        expected_query = """
            SELECT * FROM {namespace}.tb_lista_processos
            WHERE orgao_dk = :orgao_id
            ORDER BY dt_ultimo_andamento DESC
        """.format(namespace=settings.TABLE_NAMESPACE)
        expected_parameters = {
            'orgao_id': 1
        }

        _run_query.assert_called_with(expected_query, expected_parameters)
        self.assertEqual(_run_query.call_count, 2)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_1.data, expected_response_page_1)
        self.assertEqual(response_2.data, expected_response_page_2)

    @mock.patch('dominio.tutela.views.run_query')
    def test_entradas_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:lista-processos',
            args=('1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class TestTempoTramitacao(NoJWTTestCase, TestCase):
    @mock.patch('dominio.tutela.views.run_query')
    def test_correct_response(self, _run_query):
        expected = {
            "id_orgao": 12345,
            "media_orgao": 10.1243,
            "minimo_orgao": 0,
            "maximo_orgao": 100,
            "mediana_orgao": 10.2312,
            "media_pacote": 11.4352,
            "minimo_pacote": 0,
            "maximo_pacote": 200,
            "mediana_pacote": 56.3124,
            "media_pacote_t1": 45.343,
            "minimo_pacote_t1": 12,
            "maximo_pacote_t1": 533,
            "mediana_pacote_t1": 343.324,
            "media_orgao_t1": 344.12,
            "minimo_orgao_t1": 12,
            "maximo_orgao_t1": 5023,
            "mediana_orgao_t1": 2421.1223,
            "media_pacote_t2": 343.1254,
            "minimo_pacote_t2": 48,
            "maximo_pacote_t2": 2335,
            "mediana_pacote_t2": 7623.1224,
            "media_orgao_t2": 43224.1132,
            "minimo_orgao_t2": 432,
            "maximo_orgao_t2": 1324,
            "mediana_orgao_t2": 2242.3232
        }
        _run_query.return_value = [expected.values()]
        url = reverse("dominio:tempo-tramitacao", args=("1234", ))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected)


class TestNumeroDesarquivamentos(NoJWTTestCase, TestCase):
    @mock.patch("dominio.tutela.views.connections")
    def test_correct_response(self, _connections):
        cursor_mock = mock.MagicMock()
        cursor_mock.execute.return_value.fetchall.return_value\
            = [("nr_mp_1", 1), ("nr_mp_2", 2)]
        conn_mock = mock.MagicMock()
        conn_mock.cursor.return_value.__enter__.return_value = cursor_mock

        _connections.__getitem__.return_value = conn_mock
        url = reverse("dominio:desarquivamentos", args=("12345",))

        resp = self.client.get(url)
        expected = [
            {"numero_mprj": "nr_mp_1", "qtd_desarq": 1},
            {"numero_mprj": "nr_mp_2", "qtd_desarq": 2},
        ]

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected)
