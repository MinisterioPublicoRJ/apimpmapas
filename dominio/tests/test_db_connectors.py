from unittest import mock

from django.conf import settings
from django.test import TestCase

from dominio.db_connectors import execute


class TestImpalaConnector(TestCase):
    def setUp(self):
        self.expected_result = "result set"
        self.cursor_mock = mock.Mock()
        self.cursor_mock.fetchall.return_value = self.expected_result
        self.enter_conn_mock = mock.MagicMock()
        self.enter_conn_mock.cursor.return_value.__enter__.return_value\
            = self.cursor_mock

        self.connect_patcher = mock.patch("dominio.db_connectors.bda_connect")
        self.connect_mock = self.connect_patcher.start()
        self.connect_mock.return_value.__enter__.return_value\
            = self.enter_conn_mock

        self.query = "SELECT  * FROM foo;"
        self.parameters = {"a": 1, "b": 2}

    def tearDown(self):
        self.connect_patcher.stop()

    def test_connect_to_impala(self):
        result = execute(self.query, self.parameters)

        self.connect_mock.assert_called_once_with(
            host=settings.IMPALA_HOST,
            port=settings.IMPALA_PORT,
            use_ssl=False,
            user=settings.KERBEROS_USER,
            kerberos_service_name='impala',
            auth_mechanism='GSSAPI'
        )
        self.cursor_mock.execute.assert_called_once_with(
            self.query,
            self.parameters
        )
        self.assertEqual(result, self.expected_result)
