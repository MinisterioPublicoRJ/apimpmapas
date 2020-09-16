from unittest import mock


class RemoveFiltroAlertasDispensadosTestCase:
    def setUp(self):
        super().setUp()
        self.hbase_get_table_patcher = mock.patch(
            "dominio.alertas.dao.get_hbase_table"
        )
        self.hbase_table_mock = mock.Mock()
        self.hbase_table_mock.scan.return_value = []
        self.hbase_get_table_mock = self.hbase_get_table_patcher.start()
        self.hbase_get_table_mock.return_value = self.hbase_table_mock

    def tearDown(self):
        super().tearDown()
        self.hbase_get_table_patcher.stop()
