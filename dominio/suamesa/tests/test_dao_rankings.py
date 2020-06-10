from unittest import mock
import pytest

from django.test import TestCase

from dominio.dao import GenericDAO
from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase
from dominio.suamesa.dao_rankings import RankingDAO, RankingMixin
from dominio.exceptions import APIEmptyResultError


class TestRankingDAO(NoJWTTestCase, NoCacheTestCase, TestCase):
    def test_init(self):
        nome_campo = 'nome_campo_teste'

        dao = RankingDAO(nome_campo)
        self.assertEqual(dao.ranking_fieldname, nome_campo)

    @mock.patch.object(GenericDAO, "query")
    @mock.patch("dominio.suamesa.dao_rankings.impala_execute")
    def test_execute(self, _impala_execute, _query):
        _query.return_value = "SELECT {nm_campo} FROM dual"
        nome_campo = 'nome_campo_teste'

        orgao_id = 12345
        dao = RankingDAO(nome_campo)
        dao.execute(orgao_id=orgao_id)

        _impala_execute.assert_called_once_with(
            "SELECT nome_campo_teste FROM dual", {"orgao_id": orgao_id}
        )

    def test_serialize(self):
        dao = RankingDAO('teste')

        result_set = [
            ('PROMOTORIA DO RIO DE JANEIRO', '10'),
            ('OUTRA PROMOTORIA DO RIO DE JANEIRO', '5'),
        ]
        expected_result = [
            {'nm_orgao': 'Promotoria do Rio de Janeiro', 'valor': 10},
            {'nm_orgao': 'Outra Promotoria do Rio de Janeiro', 'valor': 5},
        ]

        output = dao.serialize(result_set)

        self.assertEqual(output, expected_result)

    @mock.patch("dominio.suamesa.dao_rankings.impala_execute")
    def test_get_data_OK(self, _impala_execute):
        _impala_execute.return_value = [
            ('PROMOTORIA DO RIO DE JANEIRO', '10'),
            ('OUTRA PROMOTORIA DO RIO DE JANEIRO', '5'),
        ]
        expected_result = [
            {'nm_orgao': 'Promotoria do Rio de Janeiro', 'valor': 10},
            {'nm_orgao': 'Outra Promotoria do Rio de Janeiro', 'valor': 5},
        ]

        dao = RankingDAO('teste')
        output = dao.get(accept_empty=True)

        self.assertEqual(output, expected_result)

    @mock.patch("dominio.suamesa.dao_rankings.impala_execute")
    def test_get_data_empty_accept(self, _impala_execute):
        _impala_execute.return_value = []
        expected_result = []

        dao = RankingDAO('teste')
        output = dao.get(accept_empty=True)

        self.assertEqual(output, expected_result)

    @mock.patch("dominio.suamesa.dao_rankings.impala_execute")
    def test_get_data_empty_not_accept(self, _impala_execute):
        _impala_execute.return_value = []

        dao = RankingDAO('teste')

        with pytest.raises(APIEmptyResultError):
            dao.get(accept_empty=False)


class TestRankingMixin(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch("dominio.suamesa.dao_rankings.RankingMixin.ranking_dao",
                new_callable=mock.PropertyMock)
    @mock.patch("dominio.suamesa.dao_rankings.RankingMixin.ranking_fields",
                new_callable=mock.PropertyMock)
    def test_get_ranking_data(self, _ranking_fields, _ranking_dao):
        _ranking_fields.return_value = ['campo_teste']
        dao_mock = mock.MagicMock()
        dao_mock_created = mock.MagicMock()
        dao_mock.return_value = dao_mock_created
        dao_mock_created.get.return_value = [
            {'nm_orgao': 'tal', 'valor': 1},
            {'nm_orgao': 'bla', 'valor': 2},
        ]
        _ranking_dao.return_value = dao_mock

        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste'}

        orgao_id = 10
        kwargs = {
            'orgao_id': orgao_id,
            'tipo_detalhe': 'teste',
            'n': 3,
            'intervalo': 30
        }

        output = RankingMixin.get_ranking_data(orgao_id, mock_request)
        expected_output = [
            {
                'ranking_fieldname': 'campo_teste',
                'data': [
                    {'nm_orgao': 'tal', 'valor': 1},
                    {'nm_orgao': 'bla', 'valor': 2},
                ]
            }
        ]
        self.assertEqual(output, expected_output)
        dao_mock_created.get.assert_called_once_with(
            accept_empty=True,
            **kwargs
        )

    @mock.patch("dominio.suamesa.dao_rankings.RankingMixin.ranking_dao",
                new_callable=mock.PropertyMock)
    @mock.patch("dominio.suamesa.dao_rankings.RankingMixin.ranking_fields",
                new_callable=mock.PropertyMock)
    def test_get_ranking_data_empty_accept(
            self, _ranking_fields, _ranking_dao):
        _ranking_fields.return_value = ['campo_teste']
        dao_mock = mock.MagicMock()
        dao_mock_created = mock.MagicMock()
        dao_mock.return_value = dao_mock_created
        dao_mock_created.get.return_value = []
        _ranking_dao.return_value = dao_mock

        mock_request = mock.MagicMock()
        mock_request.GET = {'tipo': 'teste'}

        orgao_id = 10
        kwargs = {
            'orgao_id': orgao_id,
            'tipo_detalhe': 'teste',
            'n': 3,
            'intervalo': 30
        }

        output = RankingMixin.get_ranking_data(orgao_id, mock_request)
        expected_output = []
        self.assertEqual(output, expected_output)
        dao_mock_created.get.assert_called_once_with(
            accept_empty=True,
            **kwargs
        )

    @mock.patch("dominio.suamesa.dao_rankings.super")
    @mock.patch.object(RankingMixin, "get_ranking_data")
    def test_get(self, _get_ranking_data, _super):
        super_mock = mock.MagicMock()
        _super.return_value = super_mock
        _get_ranking_data.return_value = [{'data': 1}]
        super_mock.get.return_value = {'metrics': {'data': 1}}

        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        output = RankingMixin.get(orgao_id, mock_request)
        expected_output = {
            'metrics': {'data': 1},
            'rankings': [{'data': 1}],
            'mapData': {}
        }

        self.assertEqual(output, expected_output)

    @mock.patch("dominio.suamesa.dao_rankings.super")
    @mock.patch.object(RankingMixin, "get_ranking_data")
    def test_get_no_data(self, _get_ranking_data, _super):
        super_mock = mock.MagicMock()
        _super.return_value = super_mock
        _get_ranking_data.return_value = []
        super_mock.get.return_value = {'metrics': {}}

        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        with pytest.raises(APIEmptyResultError):
            RankingMixin.get(orgao_id, mock_request)
