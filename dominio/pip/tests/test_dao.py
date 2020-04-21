from unittest import mock

import pytest

from dominio.exceptions import APIEmptyResultError
from dominio.pip.dao import PIPIndicadoresSucessoDAO, QUERIES_DIR


class TestPIPIndicadoresSucesso:
    @mock.patch("dominio.pip.dao.impala_execute")
    def test_execute_query(self, _impala_execute):
        with open(QUERIES_DIR.child("pip_taxa_resolutividade.sql")) as fobj:
            query = fobj.read()

        orgao_id = "12345"
        PIPIndicadoresSucessoDAO.execute(orgao_id=orgao_id)

        _impala_execute.assert_called_once_with(
            query, {"orgao_id": orgao_id}
        )

    def test_serialize_result_set(self):
        result_set = [(0.133,)]
        ser_data = PIPIndicadoresSucessoDAO.serialize(result_set)
        expected = {"taxa_resolutivdade": 0.133}

        assert ser_data == expected

    @mock.patch.object(PIPIndicadoresSucessoDAO, "execute")
    @mock.patch.object(PIPIndicadoresSucessoDAO, "serialize")
    def test_get_data(self, _serialize, _execute):
        result_set = [(0.133)]
        _execute.return_value = result_set
        _serialize.return_value = {"data": 1}

        orgao_id = "12345"
        data = PIPIndicadoresSucessoDAO.get(orgao_id=orgao_id)

        _execute.assert_called_once_with(orgao_id=orgao_id)
        _serialize.assert_called_once_with(result_set)
        assert data == {"data": 1}

    @mock.patch.object(PIPIndicadoresSucessoDAO, "execute")
    @mock.patch.object(PIPIndicadoresSucessoDAO, "serialize")
    def test_get_data_404_exception(self, _serialize, _execute):
        result_set = []
        _execute.return_value = result_set
        _serialize.return_value = {"data": 1}

        orgao_id = "12345"
        with pytest.raises(APIEmptyResultError):
            PIPIndicadoresSucessoDAO.get(orgao_id=orgao_id)

        _execute.assert_called_once_with(orgao_id=orgao_id)
        _serialize.assert_not_called
