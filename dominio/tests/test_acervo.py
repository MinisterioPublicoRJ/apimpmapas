from unittest import mock

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from dominio.views import SuaMesa
# Create your tests here.


class NoCacheTestCase:
    def tearDown(self):
        cache.clear()


class AcervoViewTest(NoCacheTestCase, TestCase):

    @mock.patch('dominio.views.run_query')
    def test_acervo_variation_result(self, _run_query):
        _run_query.return_value = [('10',), ]
        response = self.client.get(reverse(
            'dominio:acervo',
            args=('0', '1')))

        expected_response = {'acervo_qtd': 10}

        expected_query = (
            "SELECT SUM(acervo) "
            "FROM {namespace}.tb_acervo A "
            "INNER JOIN cluster.atualizacao_pj_pacote B "
            "ON A.cod_orgao = cast(B.id_orgao as int) "
            "INNER JOIN {namespace}.tb_regra_negocio_investigacao C "
            "ON C.cod_atribuicao = B.cod_pct "
            "AND C.classe_documento = A.tipo_acervo "
            "WHERE cod_orgao = 0 "
            "AND dt_inclusao = to_timestamp('1', 'yyyy-MM-dd')".format(
              namespace=settings.TABLE_NAMESPACE
            ))
        _run_query.assert_called_once_with(expected_query)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.run_query')
    def test_acervo_variation_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:acervo',
            args=('0', '1')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class AcervoVariationViewTest(NoCacheTestCase, TestCase):

    @mock.patch('dominio.views.run_query')
    def test_acervo_variation_result(self, _run_query):
        _run_query.return_value = [('100', '100', '0.0'), ]
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
                FROM {namespace}.tb_acervo tb_data_fim
                INNER JOIN (
                    SELECT
                        acervo as acervo_inicio,
                        dt_inclusao as data_inicio,
                        cod_orgao,
                        tipo_acervo
                    FROM {namespace}.tb_acervo
                    WHERE dt_inclusao = to_timestamp(
                        '1', 'yyyy-MM-dd')
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                    AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                ON regras.cod_atribuicao = tb_data_fim.cod_atribuicao
                    AND regras.classe_documento = tb_data_fim.tipo_acervo
                WHERE tb_data_fim.dt_inclusao = to_timestamp(
                    '2', 'yyyy-MM-dd')
                AND tb_data_fim.cod_orgao = 0) t
            """.format(namespace=settings.TABLE_NAMESPACE)

        _run_query.assert_called_once_with(expected_query)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.run_query')
    def test_acervo_variation_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:acervo_variation',
            args=('0', '1', '2')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class AcervoVariationTopNViewTest(NoCacheTestCase, TestCase):

    @mock.patch('dominio.views.run_query')
    def test_acervo_variation_result(self, _run_query):
        _run_query.return_value = [
            (1, 'PROMO1', '100', '50', '100.0'),
            (2, 'PROMO2', '50', '100', '-50.0'),
            (3, 'PROMO3', '300', '100', '200.0')
        ]
        response = self.client.get(reverse(
            'dominio:acervo_variation_topn',
            args=('0', '1', '2', '3')))

        expected_response = [
            {
                'cod_orgao': 1,
                'nm_orgao': 'PROMO1',
                'acervo_fim': 100,
                'acervo_inicio': 50,
                'variacao': 100.0,
            },
            {
                'cod_orgao': 2,
                'nm_orgao': 'PROMO2',
                'acervo_fim': 50,
                'acervo_inicio': 100,
                'variacao': -50.0,
            },
            {
                'cod_orgao': 3,
                'nm_orgao': 'PROMO3',
                'acervo_fim': 300,
                'acervo_inicio': 100,
                'variacao': 200.0
            }
        ]

        expected_query = """
                SELECT
                    cod_orgao,
                    orgi_nm_orgao,
                    acervo_fim,
                    acervo_inicio,
                    (acervo_fim - acervo_inicio)/acervo_inicio as variacao
                FROM (
                    SELECT
                        tb_data_fim.cod_orgao,
                        SUM(tb_data_fim.acervo) as acervo_fim,
                        SUM(tb_data_inicio.acervo_inicio) as acervo_inicio
                        FROM {namespace}.tb_acervo tb_data_fim
                    INNER JOIN (
                        SELECT
                            acervo as acervo_inicio,
                            dt_inclusao as data_inicio,
                            cod_orgao,
                            tipo_acervo
                        FROM {namespace}.tb_acervo
                        WHERE dt_inclusao = to_timestamp(
                            '1', 'yyyy-MM-dd')
                        ) tb_data_inicio
                    ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                    AND tb_data_fim.tipo_acervo = tb_data_inicio.tipo_acervo
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                    ON regras.cod_atribuicao = tb_data_fim.cod_atribuicao
                        AND regras.classe_documento = tb_data_fim.tipo_acervo
                    WHERE tb_data_fim.dt_inclusao = to_timestamp(
                        '2', 'yyyy-MM-dd')
                    GROUP BY tb_data_fim.cod_orgao
                    ) t
                INNER JOIN exadata.orgi_orgao ON orgi_orgao.orgi_dk = cod_orgao
                WHERE cod_orgao IN (
                    SELECT cast(id_orgao as int)
                    FROM cluster.atualizacao_pj_pacote A
                    INNER JOIN (
                        SELECT cod_pct
                        FROM cluster.atualizacao_pj_pacote
                        WHERE id_orgao = '0') B
                    ON A.cod_pct = B.cod_pct)
                ORDER BY variacao DESC
                LIMIT 3;
                """.format(namespace=settings.TABLE_NAMESPACE)

        _run_query.assert_called_once_with(expected_query)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    @mock.patch('dominio.views.run_query')
    def test_acervo_variation_no_result(self, _run_query):
        _run_query.return_value = []
        response = self.client.get(reverse(
            'dominio:acervo_variation_topn',
            args=('0', '1', '2', '3')))

        expected_response = {'detail': 'Não encontrado.'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


class OutliersViewTest(NoCacheTestCase, TestCase):

    @mock.patch('dominio.views.run_query')
    def test_outliers_result(self, _run_query):
        _run_query.return_value = \
            [
                (
                    '20', '100', '1000', '500', '300',
                    '450', '700', '400', '50', '950'
                ),
            ]
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
                FROM {namespace}.tb_acervo A
                INNER JOIN {namespace}.tb_distribuicao B
                ON A.cod_atribuicao = B.cod_atribuicao
                AND A.dt_inclusao = B.dt_inclusao
                WHERE A.cod_orgao = 0
                AND B.dt_inclusao = to_timestamp('1', 'yyyy-MM-dd')
                """.format(namespace=settings.TABLE_NAMESPACE)

        _run_query.assert_called_once_with(expected_query)
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
                WHERE id_orgao = 120
                """.format(namespace=settings.TABLE_NAMESPACE)

        _run_query.assert_called_once_with(expected_query)
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
                WHERE comb_orga_dk = 1
                AND comb_cdmatricula = '00000002'
                """.format(namespace=settings.TABLE_NAMESPACE)

        _run_query.assert_called_once_with(expected_query)
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

    @mock.patch('dominio.views.run_query')
    def test_sua_mesa_get_regras_investigacao(self, _run_query):
        _run_query.return_value = [(20,), (30,)]

        output = SuaMesa.get_regras(10, 'investigacao')
        expected_output = [20, 30]

        expected_query = """
            SELECT r.classe_documento
            FROM {namespace}.atualizacao_pj_pacote pct
            JOIN {namespace}.tb_regra_negocio_investigacao r
            ON r.cod_atribuicao = pct.cod_pct
            WHERE pct.id_orgao = 10
        """.format(namespace=settings.TABLE_NAMESPACE)

        _run_query.assert_called_once_with(expected_query)
        self.assertEqual(output, expected_output)

    @mock.patch('dominio.views.run_query')
    def test_sua_mesa_get_regras_processo(self, _run_query):
        _run_query.return_value = [(20,), (30,)]

        output = SuaMesa.get_regras(10, 'processo')
        expected_output = [20, 30]

        expected_query = """
            SELECT r.classe_documento
            FROM {namespace}.atualizacao_pj_pacote pct
            JOIN {namespace}.tb_regra_negocio_processo r
            ON r.cod_atribuicao = pct.cod_pct
            WHERE pct.id_orgao = 10
        """.format(namespace=settings.TABLE_NAMESPACE)

        _run_query.assert_called_once_with(expected_query)
        self.assertEqual(output, expected_output)

    @mock.patch.object(SuaMesa, 'get_regras')
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

    @mock.patch.object(SuaMesa, 'get_regras')
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


class TestSuaMesaDetalhe(TestCase):
    @mock.patch('dominio.views.Vista')
    def test_correct_response(self, _Vista):
        expected_resp = {
            'soma_ate_vinte': 25,
            'soma_vinte_trinta': 2,
            'soma_trinta_mais': 4
        }
        _Vista.vistas.abertas_por_dias_abertura.return_value = expected_resp

        url = reverse('dominio:sua_mesa_detalhe', args=('1', '2'))

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

        url = reverse('dominio:sua_mesa_detalhe', args=('1', '2'))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)
