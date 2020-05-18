from unittest import mock

from django.test import TestCase
from django.urls import reverse

from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase
from dominio.pip.utils import get_aisps


class PIPDetalheAproveitamentosViewTest(
    NoJWTTestCase, NoCacheTestCase, TestCase
):
    @mock.patch("dominio.pip.views.PIPDetalheAproveitamentosDAO.get")
    def test_correct_response_get(self, _get_data):
        _get_data.return_value = [{"data": 1}]

        url = reverse(
            "dominio:pip-aproveitamentos",
            args=("1234",)
        )
        resp = self.client.get(url)

        _get_data.assert_called_once_with(orgao_id=1234)
        assert resp.status_code == 200
        assert resp.data == [{"data": 1}]


class PIPVistasAbertasMensalTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.pip.views.Vista")
    def test_pip_vistas_abertas_mensal(self, _Vista):
        manager_mock = mock.MagicMock()
        filter_mock = mock.MagicMock()
        values_mock = mock.MagicMock()
        distinct_mock = mock.MagicMock()

        manager_mock.count.return_value = 10

        manager_mock.filter.return_value = filter_mock
        filter_mock.values.return_value = values_mock
        values_mock.distinct.return_value = distinct_mock
        distinct_mock.count.return_value = 5

        _Vista.vistas.aberturas_30_dias_PIP.return_value = manager_mock
        orgao_id = "10"
        cpf = "123456789"

        url = reverse("dominio:pip-aberturas-mensal", args=(orgao_id, cpf))
        resp = self.client.get(url)

        expected_output = {
            "nr_aberturas_30_dias": 10,
            "nr_investigacoes_30_dias": 5,
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_output)
        _Vista.vistas.aberturas_30_dias_PIP.assert_called_once_with(
            int(orgao_id), cpf
        )
        manager_mock.count.assert_called_once_with()
        distinct_mock.count.assert_called_once_with()


class PIPInvestigacoesCursoAISPTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.pip.utils.run_query")
    @mock.patch("dominio.pip.views.Documento")
    def test_pip_investigacoes_curso_aisp(self, _Documento, _run_query_aisps):
        _run_query_aisps.return_value = [
            (1, 1, "AISP1"),
            (1, 2, "AISP2"),
            (2, 1, "AISP1"),
            (2, 2, "AISP2"),
            (3, 3, "AISP3"),
            (4, 3, "AISP3"),
            (5, 3, "AISP3"),
        ]

        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 100
        _Documento.investigacoes.em_curso_pip_aisp.return_value = manager_mock

        get_aisps.cache_clear()
        orgao_id = "1"
        url = reverse(
            "dominio:pip-suamesa-investigacoes-aisp",
            args=(orgao_id,)
        )
        resp = self.client.get(url)

        expected_output = {"aisp_nr_investigacoes": 100}

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_output)
        _Documento.investigacoes.em_curso_pip_aisp.assert_called_once_with(
            {1, 2}
        )
        manager_mock.count.assert_called_once_with()


class TestPIPIndicadoresSucesso(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.pip.views.PIPRankingDenunciasDAO")
    @mock.patch("dominio.pip.views.PIPTaxaResolutividadeDAO")
    def test_correct_response(
            self, _PIPTaxaResolutividade, _PIPRankingDenuncias):
        _PIPTaxaResolutividade.get.return_value = {"data": 1}
        _PIPRankingDenuncias.get.return_value = {"ranking": 1}

        orgao_id = "12345"
        url = reverse("dominio:pip-taxa-resolutividade", args=(orgao_id,))
        resp = self.client.get(url)
        expected = {"data": 1, "ranking": 1}

        assert resp.status_code == 200
        assert resp.data == expected


class PIPSuaMesaInqueritosTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.pip.views.Documento")
    def test_pip_suamesa_inqueritos(self, _Documento):
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 100
        _Documento.investigacoes.em_curso.return_value = manager_mock

        orgao_id = "1"
        url = reverse("dominio:pip-suamesa-inqueritos", args=(orgao_id,))
        resp = self.client.get(url)

        expected_output = {"pip_nr_inqueritos": 100}

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_output)
        _Documento.investigacoes.em_curso.assert_called_once_with(
            1, [3, 494]
        )
        manager_mock.count.assert_called_once_with()


class PIPSuaMesaPICsTest(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.pip.views.Documento")
    def test_pip_suamesa_pics(self, _Documento):
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 100
        _Documento.investigacoes.em_curso.return_value = manager_mock

        orgao_id = "1"
        url = reverse("dominio:pip-suamesa-pics", args=(orgao_id,))
        resp = self.client.get(url)

        expected_output = {"pip_nr_pics": 100}

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_output)
        _Documento.investigacoes.em_curso.assert_called_once_with(
            1, [590]
        )
        manager_mock.count.assert_called_once_with()


class TestPIPRadarPerformance(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.pip.views.PIPRadarPerformanceDAO.get")
    def test_correct_response(self, _get_data):
        _get_data.return_value = {"data": 1}

        url = reverse("dominio:pip-radar-performance", args=("12345",))
        resp = self.client.get(url)

        assert resp.status_code == 200
        assert resp.data == {"data": 1}


class TestPIPPrincipaisInvestigadosView(
        NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.pip.views.PIPPrincipaisInvestigadosDAO.get")
    def test_correct_response_get(self, _get_data):
        _get_data.return_value = [{"data": 1}]

        url = reverse(
            "dominio:pip-principais-investigados",
            args=("1234", "123")
        )
        resp = self.client.get(url)

        _get_data.assert_called_once_with(orgao_id="1234", cpf="123")
        assert resp.status_code == 200
        assert resp.data == [{"data": 1}]

    @mock.patch("dominio.pip.views.PIPPrincipaisInvestigadosDAO."
                "save_hbase_flags")
    def test_correct_response_save_flags(self, _save_flags):
        _save_flags.return_value = {"data": 1}

        url = reverse(
            "dominio:pip-principais-investigados",
            args=("1234", "123")
        )
        data = {"representante_dk": "123456", "action": "qualquer"}
        resp = self.client.post(url, data)

        _save_flags.assert_called_once_with(
            "1234", "123", "123456", "qualquer"
        )
        assert resp.status_code == 200
        assert resp.data == {"data": 1}

    @mock.patch("dominio.pip.views.PIPPrincipaisInvestigadosDAO."
                "save_hbase_flags")
    def test_no_personagem_save_flags(self, _save_flags):
        _save_flags.return_value = {"data": 1}

        url = reverse(
            "dominio:pip-principais-investigados",
            args=("1234", "123")
        )
        data = {"action": "qualquer"}
        with self.assertRaises(ValueError):
            resp = self.client.post(url, data)

            _save_flags.assert_not_called()
            assert resp.status_code == 200

    @mock.patch("dominio.pip.views.PIPPrincipaisInvestigadosDAO."
                "save_hbase_flags")
    def test_no_action_save_flags(self, _save_flags):
        _save_flags.return_value = {"data": 1}

        url = reverse(
            "dominio:pip-principais-investigados",
            args=("1234", "123")
        )
        data = {"representante_dk": "123456"}
        with self.assertRaises(ValueError):
            resp = self.client.post(url, data)

            _save_flags.assert_not_called()
            assert resp.status_code == 200


class TestPIPPrincipaisInvestigadosListaView(
        NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.pip.views.PIPPrincipaisInvestigadosListaDAO.get")
    def test_correct_response(self, _get_data):
        _get_data.return_value = {"data": 1}

        url = reverse(
            "dominio:pip-principais-investigados-lista",
            args=("12345",)
        )
        resp = self.client.get(url)

        _get_data.assert_called_once_with(dk=12345)
        assert resp.status_code == 200
        assert resp.data == {"data": 1}
