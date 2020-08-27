from datetime import datetime
from unittest import mock

import pytest
from django.conf import settings

from dominio.exceptions import APIEmptyResultError
from dominio.pip.dao import (
    GenericPIPDAO,
    PIPDetalheAproveitamentosDAO,
    PIPIndicadoresDeSucessoDAO,
    PIPRadarPerformanceDAO,
    PIPPrincipaisInvestigadosDAO,
    PIPPrincipaisInvestigadosListaDAO,
)
from dominio.pip.utils import get_aisps


QUERIES_DIR = GenericPIPDAO.QUERIES_DIR


class TestPIPDetalheAproveitamentosDAO:
    @mock.patch("dominio.pip.utils.run_query")
    @mock.patch("dominio.dao.impala_execute")
    def test_pip_aproveitamentos_result(
            self, _impala_execute, _run_query_aisps):
        _impala_execute.return_value = [
            (1, "TC 1", 20, 50, 0.75, 30),
            (2, "TC 2", 30, 10, 0.5, 30),
            (3, "TC 3", 50, 40, 1.0, 30),
            (4, "TC 4", 10, 100, 0.75, 30),
            (5, "TC 5", 40, 30, 0.75, 30),
        ]
        _run_query_aisps.return_value = [
            (1, 1, "AISP1", 200),
            (1, 2, "AISP2", 200),
            (2, 1, "AISP1", 200),
            (2, 2, "AISP2", 200),
            (3, 3, "AISP3", 200),
            (4, 3, "AISP3", 200),
            (5, 3, "AISP3", 200),
        ]

        get_aisps.cache_clear()
        response = PIPDetalheAproveitamentosDAO.get(orgao_id=1)

        expected_response = {
            "nr_aproveitamentos_periodo": 20,
            "variacao_periodo": 0.75,
            "top_n_pacote": [
                {"nm_promotoria": "tc 3", "nr_aproveitamentos_periodo": 50},
                {"nm_promotoria": "tc 5", "nr_aproveitamentos_periodo": 40},
                {"nm_promotoria": "tc 2", "nr_aproveitamentos_periodo": 30},
            ],
            "nr_aisps": [1, 2],
            "top_n_aisp": [
                {"nm_promotoria": "tc 2", "nr_aproveitamentos_periodo": 30},
                {"nm_promotoria": "tc 1", "nr_aproveitamentos_periodo": 20},
            ],
            "tamanho_periodo_dias": 30,
        }

        assert response == expected_response

    @mock.patch("dominio.dao.impala_execute")
    def test_pip_aproveitamentos_no_result(self, _impala_execute):
        _impala_execute.return_value = []

        with pytest.raises(APIEmptyResultError):
            PIPDetalheAproveitamentosDAO.get(orgao_id=1)


class TestPIPRadarPerformance:
    def test_query_method(self):
        with open(QUERIES_DIR.child("pip_radar_performance.sql")) as fobj:
            query = fobj.read()

        cls = PIPRadarPerformanceDAO
        expected_query = query.format(schema=settings.TABLE_NAMESPACE)

        assert cls.query() == expected_query

    def test_serialize_result(self):
        result_set = [
            (
                16,
                "16",
                29933850,
                3,
                2,
                0,
                0,
                12,
                15,
                6,
                0,
                6,
                486,
                0.42857142857142855,
                0.3333333333333333,
                None,
                0.0,
                0.030864197530864196,
                3.0,
                5.0,
                0.0,
                0.0,
                79.0,
                0.0,
                -0.6,
                None,
                None,
                -0.810126582278481,
                datetime(2020, 4, 22, 13, 36, 6, 668000),
                "1ª PROMOTORIA DE JUSTIÇA",
                "2ª PROMOTORIA DE JUSTIÇA",
                "3ª PROMOTORIA DE JUSTIÇA",
                "4ª PROMOTORIA DE JUSTIÇa",
                "5ª PROMOTORIA DE JUSTIÇA",
                200,
            ),
        ]
        ser_data = PIPRadarPerformanceDAO.serialize(result_set)
        expected_data = {
            "aisp_codigo": 16,
            "aisp_nome": "16",
            "orgao_id": 29933850,
            "nr_denuncias": 3,
            "nr_cautelares": 2,
            "nr_acordos_n_persecucao": 0,
            "nr_arquivamentos": 0,
            "nr_aberturas_vista": 12,
            "max_aisp_denuncias": 15,
            "max_aisp_cautelares": 6,
            "max_aisp_acordos": 0,
            "max_aisp_arquivamentos": 6,
            "max_aisp_aberturas_vista": 486,
            "perc_denuncias": 0.42857142857142855,
            "perc_cautelares": 0.3333333333333333,
            "perc_acordos": None,
            "perc_arquivamentos": 0.0,
            "perc_aberturas_vista": 0.030864197530864196,
            "med_aisp_denuncias": 3.0,
            "med_aisp_cautelares": 5.0,
            "med_aisp_acordos": 0.0,
            "med_aisp_arquivamentos": 0.0,
            "med_aisp_aberturas_vista": 79.0,
            "var_med_denuncias": 0.0,
            "var_med_cautelares": -0.6,
            "var_med_acordos": None,
            "var_med_arquivamentos": None,
            "var_med_aberturas_vista": -0.810126582278481,
            "dt_calculo": datetime(2020, 4, 22, 13, 36, 6, 668000),
            "nm_max_denuncias": "1ª Promotoria de Justiça",
            "nm_max_cautelares": "2ª Promotoria de Justiça",
            "nm_max_acordos": "3ª Promotoria de Justiça",
            "nm_max_arquivamentos": "4ª Promotoria de Justiça",
            "nm_max_abeturas_vista": "5ª Promotoria de Justiça",
            "cod_pct": 200,
        }
        assert ser_data == expected_data


class TestPIPPrincipaisInvestigadosDAO:
    @mock.patch("dominio.pip.dao.get_hbase_table")
    def test_get_hbase_flags(self, _get_table):
        table_mock = mock.MagicMock()
        table_mock.scan.return_value = [
            (
                b"1",
                {
                    b"identificacao:representante_dk": b"1234",
                    b"flags:is_pinned": b"True",
                    b"flags:is_removed": b"False"
                }
            ),
            (
                b"2",
                {
                    b"identificacao:representante_dk": b"123",
                    b"flags:is_pinned": b"True"
                }
            )
        ]
        _get_table.return_value = table_mock

        expected_output = {
            1234: {"is_pinned": True, "is_removed": False},
            123: {"is_pinned": True, "is_removed": False},
        }

        data = PIPPrincipaisInvestigadosDAO.get_hbase_flags("1", "2")

        hbspace = settings.PROMOTRON_HBASE_NAMESPACE
        _get_table.assert_called_once_with(hbspace + "pip_investigados_flags")
        table_mock.scan.assert_called_once_with(row_prefix=b"12")
        assert data == expected_output

    @mock.patch("dominio.pip.dao.get_hbase_table")
    def test_save_hbase_flags_pin(self, _get_table):
        table_mock = mock.MagicMock()
        table_mock.put.return_value = None
        _get_table.return_value = table_mock

        expected_output = {"status": "Success!"}

        expected_call_arguments = {
            b"identificacao:orgao_id": b"1",
            b"identificacao:cpf": b"2",
            b"identificacao:representante_dk": b"1234",
            b"flags:is_pinned": b"True"
        }

        data = PIPPrincipaisInvestigadosDAO.save_hbase_flags(
            "1", "2", "1234", "pin")

        hbspace = settings.PROMOTRON_HBASE_NAMESPACE
        _get_table.assert_called_once_with(hbspace + "pip_investigados_flags")
        table_mock.put.assert_called_once_with(
            b"121234", expected_call_arguments)
        assert expected_output == data

    @mock.patch("dominio.pip.dao.get_hbase_table")
    def test_save_hbase_flags_remove(self, _get_table):
        table_mock = mock.MagicMock()
        table_mock.put.return_value = None
        _get_table.return_value = table_mock

        expected_output = {"status": "Success!"}

        expected_call_arguments = {
            b"identificacao:orgao_id": b"1",
            b"identificacao:cpf": b"2",
            b"identificacao:representante_dk": b"1234",
            b"flags:is_removed": b"True"
        }

        data = PIPPrincipaisInvestigadosDAO.save_hbase_flags(
            "1", "2", "1234", "remove")

        hbspace = settings.PROMOTRON_HBASE_NAMESPACE
        _get_table.assert_called_once_with(hbspace + "pip_investigados_flags")
        table_mock.put.assert_called_once_with(
            b"121234", expected_call_arguments)
        assert expected_output == data

    @mock.patch("dominio.pip.dao.get_hbase_table")
    def test_save_hbase_flags_unpin(self, _get_table):
        table_mock = mock.MagicMock()
        table_mock.delete.return_value = None
        _get_table.return_value = table_mock

        expected_output = {"status": "Success!"}

        data = PIPPrincipaisInvestigadosDAO.save_hbase_flags(
            "1", "2", "1234", "unpin")

        hbspace = settings.PROMOTRON_HBASE_NAMESPACE
        _get_table.assert_called_once_with(hbspace + "pip_investigados_flags")
        table_mock.delete.assert_called_once_with(
            b"121234", columns=["flags:is_pinned"])
        assert expected_output == data

    @mock.patch("dominio.pip.dao.get_hbase_table")
    def test_save_hbase_flags_unremove(self, _get_table):
        table_mock = mock.MagicMock()
        table_mock.delete.return_value = None
        _get_table.return_value = table_mock

        expected_output = {"status": "Success!"}

        data = PIPPrincipaisInvestigadosDAO.save_hbase_flags(
            "1", "2", "1234", "unremove")

        hbspace = settings.PROMOTRON_HBASE_NAMESPACE
        _get_table.assert_called_once_with(hbspace + "pip_investigados_flags")
        table_mock.delete.assert_called_once_with(
            b"121234", columns=["flags:is_removed"])
        assert expected_output == data

    @mock.patch.object(PIPPrincipaisInvestigadosDAO, "get_hbase_flags")
    @mock.patch.object(GenericPIPDAO, "get")
    def test_get(self, _get, _get_hbase):
        _get_hbase.return_value = {
            "1278": {"is_pinned": True, "is_removed": False},
            "5678": {"is_pinned": False, "is_removed": True},
        }
        _get.return_value = [
            {
                "nm_investigado": "Nome1",
                "representante_dk": "1234",
                "pip_codigo": 1,
                "nr_investigacoes": 10,
                "flag_multipromotoria": None,
                "flag_top50": True,
            },
            {
                "nm_investigado": "Nome2",
                "representante_dk": "1278",
                "pip_codigo": 1,
                "nr_investigacoes": 5,
                "flag_multipromotoria": True,
                "flag_top50": None,
            },
            {
                "nm_investigado": "Nome3",
                "representante_dk": "5678",
                "pip_codigo": 1,
                "nr_investigacoes": 15,
                "flag_multipromotoria": None,
                "flag_top50": None,
            },
        ]

        expected_output = [
            {
                "nm_investigado": "Nome2",
                "representante_dk": "1278",
                "pip_codigo": 1,
                "nr_investigacoes": 5,
                "flag_multipromotoria": True,
                "flag_top50": None,
                "is_pinned": True,
                "is_removed": False
            },
            {
                "nm_investigado": "Nome1",
                "representante_dk": "1234",
                "pip_codigo": 1,
                "nr_investigacoes": 10,
                "flag_multipromotoria": None,
                "flag_top50": True,
                "is_pinned": False,
                "is_removed": False
            },
        ]

        data = PIPPrincipaisInvestigadosDAO.get("1", "2")
        assert data == expected_output


class TestPIPIndicadoresSucesso:
    @mock.patch("dominio.dao.impala_execute")
    def test_execute_query(self, _impala_execute):
        with open(QUERIES_DIR.child("pip_indicadores_sucesso.sql")) as fobj:
            query = fobj.read()

        cls = PIPIndicadoresDeSucessoDAO
        query = query.format(schema=cls.table_namespaces["schema"])
        orgao_id = "12345"
        cls.execute(orgao_id=orgao_id)

        _impala_execute.assert_called_once_with(
            query, {"orgao_id": orgao_id}
        )
        assert cls.table_namespaces["schema"] == settings.TABLE_NAMESPACE

    def test_serialize_result_set(self):
        result_set = [
            ("12345", 0.344, "p_finalizacoes"),
            ("12345", 0.123, "p_resolutividade"),
            ("12345", 0.983, "p_eludcidacoes"),
        ]
        ser_data = PIPIndicadoresDeSucessoDAO.serialize(result_set)
        expected = [
            {"orgao_id": 12345, "indice": 0.344, "tipo": "p_finalizacoes"},
            {"orgao_id": 12345, "indice": 0.123, "tipo": "p_resolutividade"},
            {"orgao_id": 12345, "indice": 0.983, "tipo": "p_eludcidacoes"},
        ]

        assert ser_data == expected

    @mock.patch.object(PIPIndicadoresDeSucessoDAO, "execute")
    def test_get_data(self, _execute):
        _execute.return_value = [
            ("12345", 0.344, "p_finalizacoes"),
            ("12345", 0.123, "p_resolutividade"),
            ("12345", 0.983, "p_eludcidacoes"),
        ]

        expected = [
            {"orgao_id": 12345, "indice": 0.344, "tipo": "p_finalizacoes"},
            {"orgao_id": 12345, "indice": 0.123, "tipo": "p_resolutividade"},
            {"orgao_id": 12345, "indice": 0.983, "tipo": "p_eludcidacoes"},
        ]
        data = PIPIndicadoresDeSucessoDAO.get()

        assert data == expected


class TestPIPPrincipaisInvestigadosListaDAO:
    def test_serialize_result(self):
        result_set = [
            (
                16,
                "Nome",
                "Tipo",
                29933850,
                "123456",
                datetime(2020, 4, 22, 13, 36, 6, 668000),
                "Classe",
                "5ª PROMOTORIA DE JUSTIÇA",
                "Etiqueta",
                "Assunto 1 --- Assunto 2",
                "FaseDoc"
            ),
        ]
        ser_data = PIPPrincipaisInvestigadosListaDAO.serialize(result_set)
        expected_data = [{
            "representante_dk": 16,
            "nm_investigado": "Nome",
            "tipo_personagem": "Tipo",
            "orgao_id": 29933850,
            "documento_nr_mp": "123456",
            "documento_dt_cadastro": '2020-04-22T13:36:06.668000Z',
            "documento_classe": "Classe",
            "nm_orgao": "5ª Promotoria de Justiça",
            "etiqueta": "Etiqueta",
            "assuntos": ["Assunto 1", "Assunto 2"],
            "fase_documento": "FaseDoc"
        }]
        assert ser_data == expected_data
