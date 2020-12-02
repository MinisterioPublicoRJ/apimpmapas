from unittest import mock

from django.test import TestCase

from dominio.login.dao import AtribuicoesOrgaosDAO


class TestAtribuicaoDAO(TestCase):
    def setUp(self):
        self.ids_orgaos = ['1234', '5678']

        self.impala_execute_patcher = mock.patch(
            "dominio.login.dao.impala_execute"
        )
        self.impala_execute_mock = self.impala_execute_patcher.start()

        self.dao_query_patcher = mock.patch.object(
            AtribuicoesOrgaosDAO,
            "query"
        )
        self.dao_query_mock = self.dao_query_patcher.start()
        self.dao_query_mock.return_value = """
            SELECT * FROM foo
            WHERE id_orgao in :ids_orgaos
        """
        self.expected_query = """
            SELECT * FROM foo
            WHERE id_orgao in (1234,5678)
        """

    def tearDown(self):
        self.impala_execute_patcher.stop()
        self.dao_query_patcher.stop()

    def test_prepared_list_of_orgaos(self):
        AtribuicoesOrgaosDAO.get(ids_orgaos=self.ids_orgaos)

        self.impala_execute_mock.assert_called_once_with(
            self.expected_query,
            {"ids_orgaos": self.ids_orgaos}
        )
