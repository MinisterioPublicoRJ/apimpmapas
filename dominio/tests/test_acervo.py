from datetime import datetime, timedelta
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from dominio.views import DetalheAcervoView
from dominio.views import DetalheProcessosJuizoView

from .testconf import NoJWTTestCase, NoCacheTestCase


# Create your tests here.
class DetalheAcervoViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    def test_get_variacao_orgao_return_none(self):
        view = DetalheAcervoView()
        resp = view.get_variacao_orgao([], orgao_id=10)

        self.assertTrue(resp is None)

    @mock.patch('dominio.views.run_query')
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

        dt_inicio = datetime.now().date() - timedelta(30)
        dt_inicio = '2020-02-10' if datetime(2020, 2, 10).date() > dt_inicio \
            else str(dt_inicio)
        expected_parameters = {
            'orgao_id': 0,
            'dt_inicio': dt_inicio,
            'dt_fim': str(datetime.now().date())
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.run_query')
    def test_acervo_variation_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:suamesa-detalhe-investigacoes',
            args=('0')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class OutliersViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    @mock.patch('dominio.views.run_query')
    def test_outliers_result(self, _run_query):
        _run_query.side_effect = \
            [
                [(
                    '20', '100', '1000', '500', '300',
                    '450', '700', '400', '50', '950'
                )],
                [('10',)],
            ]
        response = self.client.get(reverse(
            'dominio:outliers',
            args=('0', '1')))

        expected_response = {
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
            'hout': 950
        }

        expected_call_outliers = mock.call("""
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
                FROM {namespace}.tb_acervo A
                INNER JOIN {namespace}.tb_distribuicao B
                ON A.cod_atribuicao = B.cod_atribuicao
                AND A.dt_inclusao = B.dt_inclusao
                WHERE A.cod_orgao = :orgao_id
                AND B.dt_inclusao = to_timestamp(:dt_calculo, 'yyyy-MM-dd')
                """.format(namespace=settings.TABLE_NAMESPACE),
                {
                    'orgao_id': 0,
                    'dt_calculo': '1'
                }
                )

        expected_call_acervo = mock.call(
            "SELECT SUM(acervo) "
            "FROM {namespace}.tb_acervo A "
            "INNER JOIN cluster.atualizacao_pj_pacote B "
            "ON A.cod_orgao = cast(B.id_orgao as int) "
            "INNER JOIN {namespace}.tb_regra_negocio_investigacao C "
            "ON C.cod_atribuicao = B.cod_pct "
            "AND C.classe_documento = A.tipo_acervo "
            "WHERE cod_orgao = :orgao_id "
            "AND dt_inclusao = to_timestamp(:data, 'yyyy-MM-dd')".format(
              namespace=settings.TABLE_NAMESPACE),
            {
                'orgao_id': 0,
                'data': '1'
            }
        )

        _run_query.assert_has_calls([
            expected_call_outliers,
            expected_call_acervo])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.run_query')
    def test_outliers_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:outliers',
            args=('0', '1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class SaidasViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    @mock.patch('dominio.views.run_query')
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

    @mock.patch('dominio.views.run_query')
    def test_saidas_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:saidas',
            args=('120',)))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class EntradasViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    @mock.patch('dominio.views.run_query')
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

    @mock.patch('dominio.views.run_query')
    def test_entradas_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:entradas',
            args=('1', '2')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class DetalheProcessosJuizoViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):

    def test_get_value_from_orgao(self):
        test_orgao_id = 42
        test_list = [
            (1, 'Nome1', 220),
            (10, 'Nome2', 140),
            (42, 'Nome3', 150),
            (60, 'Nome4', 65)
        ]
        output = DetalheProcessosJuizoView.get_value_from_orgao(
            test_list, test_orgao_id, value_position=2)
        expected_output = 150

        self.assertEqual(output, expected_output)

    def test_get_value_from_invalid_orgao(self):
        test_orgao_id = 33
        test_list = [
            (1, 'Nome1', 220),
            (10, 'Nome2', 140),
            (42, 'Nome3', 150),
            (60, 'Nome4', 65)
        ]
        output = DetalheProcessosJuizoView.get_value_from_orgao(
            test_list, test_orgao_id, value_position=2)
        expected_output = None

        self.assertEqual(output, expected_output)

    def test_get_top_n_orgaos(self):
        test_list = [
            (1, 'Nome1', 220, 0.5, 10),
            (10, 'Nome2', 140, 0.3, 5),
            (42, 'Nome3', 150, -0.10, 20),
            (60, 'Nome4', 65, 1.0, 2)
        ]
        output = DetalheProcessosJuizoView.get_top_n_orgaos(test_list, n=3)
        expected_output = [
            {'nm_promotoria': 'Nome3', 'nr_acoes_propostas_30_dias': 20},
            {'nm_promotoria': 'Nome1', 'nr_acoes_propostas_30_dias': 10},
            {'nm_promotoria': 'Nome2', 'nr_acoes_propostas_30_dias': 5}
        ]

        self.assertEqual(output, expected_output)

    @mock.patch('dominio.views.run_query')
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

    @mock.patch('dominio.views.run_query')
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

    @mock.patch('dominio.views.run_query')
    def test_detalhe_processos_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:suamesa-detalhe-processos',
            args=('1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class ListaProcessosViewTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.views.ListaProcessosView.PROCESSOS_SIZE')
    @mock.patch('dominio.views.run_query')
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

    @mock.patch('dominio.views.run_query')
    def test_entradas_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:lista-processos',
            args=('1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)
