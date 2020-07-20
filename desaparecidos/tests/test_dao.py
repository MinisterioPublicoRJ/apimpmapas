from datetime import datetime
from unittest import TestCase, mock
from textwrap import dedent

from desaparecidos.dao import (
    format_query,
    rank_query,
    serialize,
    rank,
)


class Dao(TestCase):
    def test_format_rank_query(self):
        query = """
            SELECT * FROM table WHERE id_sinalid = '{{ id_sinalid }}'
        """

        id_sinalid = "1234"
        formatted_query = format_query(query, id_sinalid)
        expected_query = """
            SELECT * FROM table WHERE id_sinalid = '1234'
        """

        self.assertEqual(formatted_query, expected_query)

    def test_format_query_filter_keep_ds(self):
        query = """
            SELECT * FROM table WHERE id_sinalid = '{{ id_sinalid }}'
            WHERE{{ filter }}
        """

        id_sinalid = "1234IM"
        formatted_query = format_query(query, id_sinalid)
        expected_query = """
            SELECT * FROM table WHERE id_sinalid = '1234IM'
            WHERE
        SELECT
            SNCA1.SNCA_DK
        FROM
            SILD_DESAPARECIMENTO SDES
        INNER JOIN
            SILD_SINDICANCIA SNCA1
        ON (SNCA1.SNCA_DK = SDES.SDES_SNCA_DK AND
            SNCA1.SNCA_SISI_DK IN (1,3))
        """

        self.assertEqual(
            dedent(formatted_query).strip(),
            dedent(expected_query).strip()
        )

    def test_format_query_filter_remove_ds(self):
        query = """
            SELECT * FROM table WHERE id_sinalid = '{{ id_sinalid }}'
            WHERE{{ filter }}
        """

        id_sinalid = "1234DS"
        formatted_query = format_query(query, id_sinalid)
        expected_query = """
            SELECT * FROM table WHERE id_sinalid = '1234DS'
            WHERE
        SELECT
            SNCA2.SNCA_DK
        FROM
                SILD_INDICA_DESAPARECIMENTO SIDS
        INNER JOIN
                SILD_SINDICANCIA SNCA2
        ON (SNCA2.SNCA_DK = SIDS.SIDS_SNCA_DK AND
            SNCA2.SNCA_SISI_DK IN (1,3,4))
        INNER JOIN
                SILD_VITIMA VTMA
        ON (VTMA.VTMA_DK = SNCA2.SNCA_VTMA_DK AND
                (VTMA.VTMA_CPF IS NULL OR
                 VTMA.VTMA_NM_VITIMA IS NULL AND
                 VTMA.VTMA_DT_NASCIMENTO IS NULL))
        """

        self.assertEqual(
            dedent(formatted_query).strip(),
            dedent(expected_query).strip()
        )

    @mock.patch("desaparecidos.dao.q_rank")
    @mock.patch('desaparecidos.dao.format_query',
                return_value="formatted query")
    def test_rank_query(self, _format_query, _query):
        cursor_mock = mock.MagicMock()
        cursor_mock.fetchall.return_value = [(1, 2, 3), (4, 5, 6)]

        id_sinalid = "1234"
        result = rank_query(cursor_mock, id_sinalid)

        _format_query.assert_called_once_with(_query, id_sinalid)
        cursor_mock.execute.assert_called_once_with("formatted query")
        cursor_mock.fetchall.assert_called_once_with()
        self.assertEqual(result, [(1, 2, 3), (4, 5, 6)])

    def test_serialize_to_json(self):
        oracle_resp = [
            (
                1,
                datetime(2017, 4, 27, 0, 0),
                "foto b64",
                74,
                "COR",
                "altura",
                "bairro 1",
                "cidade 1",
                "uf 1",
                'id 1',
                'id 2',
                datetime(1941, 4, 27, 0, 0),
                0.01,
                0,
                0,
                0,
                0.01
            ),
            (
                2,
                datetime(2010, 4, 27, 0, 0),
                "foto b64",
                32,
                "COR",
                "altura",
                "bairro 2",
                "cidade 2",
                "uf 2",
                'id 3',
                'id 4',
                datetime(1972, 4, 27, 0, 0),
                0.01,
                0,
                0,
                0,
                0.01
            ),
        ]

        resp_json = serialize(oracle_resp)
        expected = [
            {
                "snca_dk_cand": 1,
                "data_fato_cand": "2017-04-27T00:00:00",
                "foto_cand": "foto b64",
                "idade_cand": 74,
                "cor_pele_cand": "COR",
                "altura_cand": "altura",
                "bairro_cand": "bairro 1",
                "cidade_cand": "cidade 1",
                "uf_cand": "uf 1",
                "busca_id_sinalid": "id 1",
                "candidato_id_sinalid": "id 2",
                "data_nascimento": "1941-04-27T00:00:00",
                "score_sexo": 0.01,
                "score_data_fato": 0,
                "score_idade": 0,
                "score_distancia": 0,
                "score_total": 0.01
            },

            {
                "snca_dk_cand": 2,
                "data_fato_cand": "2010-04-27T00:00:00",
                "foto_cand": "foto b64",
                "idade_cand": 32,
                "cor_pele_cand": "COR",
                "altura_cand": "altura",
                "bairro_cand": "bairro 2",
                "cidade_cand": "cidade 2",
                "uf_cand": "uf 2",
                "busca_id_sinalid": "id 3",
                "candidato_id_sinalid": "id 4",
                "data_nascimento": "1972-04-27T00:00:00",
                "score_sexo": 0.01,
                "score_data_fato": 0,
                "score_idade": 0,
                "score_distancia": 0,
                "score_total": 0.01
            }
        ]

        self.assertEqual(resp_json, expected)

    @mock.patch("desaparecidos.dao.serialize", return_value="ser result")
    @mock.patch("desaparecidos.dao.rank_query", return_value="result")
    def test_whole_workflow(self, _rank_query, _serialize):
        cursor = mock.MagicMock()
        id_sinalid = "1234"

        result = rank(cursor, id_sinalid)

        _rank_query.assert_called_once_with(cursor, id_sinalid)
        _serialize.assert_called_once_with("result", 100)
        self.assertEqual(result, "ser result")

    @mock.patch("desaparecidos.dao.serialize", return_value="ser result")
    @mock.patch("desaparecidos.dao.rank_query", return_value="result")
    def test_whole_workflow_with_limit(self, _rank_query, _serialize):
        cursor = mock.MagicMock()
        id_sinalid = "1234"

        result = rank(cursor, id_sinalid, limit=200)

        _rank_query.assert_called_once_with(cursor, id_sinalid)
        _serialize.assert_called_once_with("result", 200)
        self.assertEqual(result, "ser result")

    @mock.patch("desaparecidos.dao.serialize")
    @mock.patch("desaparecidos.dao.rank_query", return_value=[])
    def test_whole_workflow_empty_response(self, _rank_query, _serialize):
        cursor = mock.MagicMock()
        id_sinalid = "1234"

        result = rank(cursor, id_sinalid, limit=200)

        _rank_query.assert_called_once_with(cursor, id_sinalid)
        _serialize.assert_not_called()
        self.assertEqual(result, {'erro': 'ID Sinalid não encontrado'})
