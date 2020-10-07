from unittest import mock

from django.test import TestCase
from django.urls import reverse

from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase


class TestPIPIndicadoresSucesso(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.pip.views.PIPIndicadoresDeSucessoDAO.execute")
    def test_correct_response(self, _execute):
        _execute.return_value = [
            ("12345", 0.344, "p_finalizacoes"),
            ("12345", 0.123, "p_resolutividade"),
            ("12345", 0.983, "p_eludcidacoes"),
        ]
        orgao_id = "12345"
        url = reverse("dominio:pip-indicadores-sucesso", args=(orgao_id,))
        resp = self.client.get(url)
        expected = [
            {"orgao_id": 12345, "indice": 0.344, "tipo": "p_finalizacoes"},
            {"orgao_id": 12345, "indice": 0.123, "tipo": "p_resolutividade"},
            {"orgao_id": 12345, "indice": 0.983, "tipo": "p_eludcidacoes"},
        ]

        assert resp.status_code == 200
        assert resp.data == expected


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
    @mock.patch("dominio.pip.views.PIPPrincipaisInvestigadosPerfilDAO.get")
    @mock.patch("dominio.pip.views.PIPPrincipaisInvestigadosListaDAO.get")
    def test_correct_response(self, _get_procedimentos, _get_perfil):
        _get_perfil.return_value = [{"data": 1}]
        _get_procedimentos.return_value = [{"data": 1}, {"data": 2}]
        expected_output = {
            "perfil": {"data": 1},
            "similares": [{"data": 1}],
            "procedimentos": [{"data": 1}, {"data": 2}]
        }

        url = reverse(
            "dominio:pip-principais-investigados-lista",
            args=("12345",)
        )
        resp = self.client.get(url)

        _get_perfil.assert_called_once_with(dk=12345)
        _get_procedimentos.assert_called_once_with(dk=12345, pess_dk=0)
        assert resp.status_code == 200
        assert resp.data == expected_output


class TestComparadorRadares(NoJWTTestCase, TestCase):
    @mock.patch("dominio.pip.views.PIPComparadorRadaresDAO.execute")
    def test_correct_response(self, _execute):
        _execute.return_value = [
            (
                "3456",
                "2ª PJ",
                "2ª PROMOTORIA",
                1.0,
                0.0,
                None,
                0.7,
                None
            ),
            (
                "6789",
                "1ª PJ",
                "1ª PROMOTORIA",
                1.0,
                1.0,
                None,
                1.0,
                None
            )
        ]
        url = reverse("dominio:pip-comparador-radares", args=("12345",))
        resp = self.client.get(url)
        expected_data = [
            {
                "orgao_id": "3456",
                "orgao_codamp": "2ª PJ",
                "orgi_nm_orgao": "2ª PROMOTORIA",
                "perc_denuncias": 1.0,
                "perc_cautelares": 0.0,
                "perc_acordos": None,
                "perc_arquivamentos": 0.7,
                "perc_aberturas_vista": None
            },
            {
                "orgao_id": "6789",
                "orgao_codamp": "1ª PJ",
                "orgi_nm_orgao": "1ª PROMOTORIA",
                "perc_denuncias": 1.0,
                "perc_cautelares": 1.0,
                "perc_acordos": None,
                "perc_arquivamentos": 1.0,
                "perc_aberturas_vista": None
            }
        ]

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, expected_data)
