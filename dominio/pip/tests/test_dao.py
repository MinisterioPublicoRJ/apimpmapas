from unittest import mock

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
