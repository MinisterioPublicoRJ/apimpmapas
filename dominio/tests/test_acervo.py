from unittest import mock

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from dominio.views import DetalheAcervoView
from dominio.views import DetalheProcessosJuizoView

# Create your tests here.


class NoCacheTestCase:
    def tearDown(self):
        cache.clear()


class DetalheAcervoViewTest(NoCacheTestCase, TestCase):
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
            'dominio:detalhe_acervo',
            args=('0', '1', '2', '3')))

        expected_response = {
            "variacao_acervo": -60.0,
            "top_n": [
                {
                    'nm_promotoria': 'PROMO3',
                    'variacao_acervo': 200.0,
                },
                {
                    'nm_promotoria': 'PROMO1',
                    'variacao_acervo': 100.0,
                },
                {
                    'nm_promotoria': 'PROMO2',
                    'variacao_acervo': -50.0,
                }
            ]
        }

        expected_query = """
                WITH tb_acervo_orgao_pct as (
                    SELECT *
                    FROM {namespace}.tb_acervo ac
                    INNER JOIN (
                        SELECT cod_pct, orgi_nm_orgao as nm_orgao
                        FROM {namespace}.atualizacao_pj_pacote
                        WHERE id_orgao = :orgao_id
                        ) org
                    ON org.cod_pct = ac.cod_atribuicao)
                SELECT
                    tb_data_fim.cod_orgao,
                    tb_data_fim.nm_orgao,
                    tb_data_fim.acervo_fim,
                    tb_data_inicio.acervo_inicio,
                    (acervo_fim - acervo_inicio)/acervo_inicio as variacao
                FROM (
                    SELECT cod_orgao, nm_orgao, SUM(acervo) as acervo_fim
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_fim, 'yyyy-MM-dd')
                    GROUP BY cod_orgao, nm_orgao
                    ) tb_data_fim
                INNER JOIN (
                    SELECT cod_orgao, nm_orgao, SUM(acervo) as acervo_inicio
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_inicio, 'yyyy-MM-dd')
                    GROUP BY cod_orgao, nm_orgao
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                """.format(namespace=settings.TABLE_NAMESPACE)

        expected_parameters = {
            'orgao_id': 0,
            'dt_inicio': '1',
            'dt_fim': '2'
        }

        _run_query.assert_called_once_with(expected_query, expected_parameters)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.run_query')
    def test_acervo_variation_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:detalhe_acervo',
            args=('0', '1', '2', '3')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class OutliersViewTest(NoCacheTestCase, TestCase):

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


class SaidasViewTest(NoCacheTestCase, TestCase):

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


class EntradasViewTest(TestCase, NoCacheTestCase):

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


class SuaMesaViewTest(TestCase, NoCacheTestCase):
    @mock.patch('dominio.views.suamesa.get_regras')
    @mock.patch('dominio.views.Documento')
    def test_sua_mesa_investigacoes(self, _Documento, _get_regras):
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 1
        _Documento.investigacoes.em_curso.return_value = manager_mock
        orgao_id = '10'
        regras = [(30,), (50,)]
        _get_regras.return_value = regras

        url = reverse('dominio:suamesa-investigacoes', args=(orgao_id, ))
        resp = self.client.get(url)

        self.assertEqual(resp.data, {"suamesa_investigacoes": 1})
        self.assertEqual(resp.status_code, 200)
        _get_regras.assert_called_once_with(int(orgao_id), tipo='investigacao')
        _Documento.investigacoes.em_curso.assert_called_once_with(
            int(orgao_id), regras
        )
        manager_mock.count.assert_called_once_with()

    @mock.patch('dominio.views.suamesa.get_regras')
    @mock.patch('dominio.views.Documento')
    def test_sua_mesa_processos(self, _Documento, _get_regras):
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 1
        _Documento.processos.em_juizo.return_value = manager_mock
        orgao_id = '10'
        regras = [(30,), (50,)]
        _get_regras.return_value = regras

        url = reverse('dominio:suamesa-processos', args=(orgao_id, ))
        resp = self.client.get(url)

        self.assertEqual(resp.data, {"suamesa_processos": 1})
        self.assertEqual(resp.status_code, 200)
        _get_regras.assert_called_once_with(int(orgao_id), tipo='processo')
        _Documento.processos.em_juizo.assert_called_once_with(
            int(orgao_id), regras
        )
        manager_mock.count.assert_called_once_with()

    @mock.patch('dominio.views.SubAndamento')
    def test_sua_mesa_finalizados(self, _SubAndamento):
        regras_saidas = (6251, 6657, 6655, 6644, 6326)
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 1
        _SubAndamento.finalizados.trinta_dias.return_value = manager_mock
        orgao_id = '10'

        url = reverse('dominio:suamesa-finalizados', args=(orgao_id, ))
        resp = self.client.get(url)

        self.assertEqual(resp.data, {"suamesa_finalizados": 1})
        self.assertEqual(resp.status_code, 200)
        _SubAndamento.finalizados.trinta_dias.assert_called_once_with(
            int(orgao_id), regras_saidas
        )
        manager_mock.count.assert_called_once_with()

    @mock.patch('dominio.views.Vista')
    def test_sua_mesa_vistas_abertas(self, _Vista):
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 1
        _Vista.vistas.abertas_promotor.return_value = manager_mock
        orgao_id = '10'
        cpf = '123456789'

        url = reverse('dominio:suamesa-vistas', args=(orgao_id, cpf))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {"suamesa_vistas": 1})
        _Vista.vistas.abertas_promotor.assert_called_once_with(
            int(orgao_id), cpf
        )
        manager_mock.count.assert_called_once_with()


class TestSuaMesaDetalheVitas(TestCase):
    @mock.patch('dominio.views.Vista')
    def test_correct_response(self, _Vista):
        expected_resp = {
            'soma_ate_vinte': 25,
            'soma_vinte_trinta': 2,
            'soma_trinta_mais': 4
        }
        _Vista.vistas.abertas_por_dias_abertura.return_value = expected_resp

        url = reverse('dominio:suamesa-detalhe-vistas', args=('1', '2'))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_resp)

    @mock.patch('dominio.views.Vista')
    def test_404_response(self, _Vista):
        query_resp = {
            'soma_ate_vinte': None,
            'soma_vinte_trinta': None,
            'soma_trinta_mais': None
        }
        _Vista.vistas.abertas_por_dias_abertura.return_value = query_resp

        url = reverse('dominio:suamesa-detalhe-vistas', args=('1', '2'))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)


class DetalheProcessosJuizoViewTest(TestCase, NoCacheTestCase):

    def test_get_nr_acoes_orgao():
        pass

    def test_get_top_n_orgaos():
        pass

    @mock.patch('dominio.views.run_query')
    def test_get_numero_acoes_propostas_pacote_atribuicao(self, _run_query):
        DetalheProcessosJuizoView.get_numero_acoes_propostas_pacote_atribuicao(1, 2, 3)

        expected_query = ""
        _run_query.assert_called_once_with(expected_query)


    @mock.patch('dominio.views.run_query')
    def test_get_porcentagem_aumento_acoes_promotoria(self, _run_query):
        DetalheProcessosJuizoView.get_porcentagem_aumento_acoes_promotoria(1, 2, 3)

        expected_query = ""
        _run_query.assert_called_once_with(expected_query)

    @mock.patch('dominio.views.run_query')
    def test_detalhe_processos_result(self, _run_query):
        _run_query.side_effect = \
            [
                [(1, 50), (2, 30), (3, 40), (4, 100), (5, 20)],
                [(10, 20, 1.0)]
            ]
        response = self.client.get(reverse(
            'dominio:detalhe_processos',
            args=('1', '2', '3')))

        expected_response = {
            'nr_acoes_propostas': 20,
            'variacao': 1.0,
            'top_n': [
                {'nome': 'TC 4', 'nr_acoes': 100},
                {'nome': 'TC 1', 'nr_acoes': 50},
                {'nome': 'TC 3', 'nr_acoes': 40}]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.run_query')
    def test_detalhe_processos_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:detalhe_processos',
            args=('1', '2', '3')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)

