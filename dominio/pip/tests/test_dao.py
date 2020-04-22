from unittest import mock

from dominio.pip.dao import PIPRadarPerformanceDAO, QUERIES_DIR


class TestPIPRadarPerformance:
    @mock.patch("dominio.pip.dao.impala_execute")
    def test_execute_query(self, _impalaa_execute):
        with open(QUERIES_DIR.child("pip_radar_performance.sql")) as fobj:
            query = fobj.read()

        orgao_id = "12345"
        PIPRadarPerformanceDAO.execute(orgao_id=orgao_id)

        _impalaa_execute.assert_called_once_with(
            query, {"orgao_id": orgao_id}
        )
