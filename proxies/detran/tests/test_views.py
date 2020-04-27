from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class TestDetranProxyView(TestCase):
    @mock.patch("proxies.detran.views.ImpalaGate")
    @mock.patch("proxies.detran.views.HBaseGate")
    @mock.patch("proxies.detran.views.DataTrafficController")
    def test_correct_response(self, _DataController, _HBase, _Impala):
        _HBase.return_value = "hbase object"
        _Impala.return_value = "impala object"
        controller_mock = mock.Mock()
        controller_mock.get_data.return_value = {"data": 1}
        _DataController.return_value = controller_mock

        rg = "12345"
        url = reverse("proxies:foto-detran", kwargs={"rg": rg})
        resp = self.client.get(url)

        _DataController.assert_called_once_with(
            rg=rg,
            data_dao=_Impala.return_value,
            photo_dao=_HBase.return_value,
        )
        _Impala.assert_called_once_with(
            table_name=settings.IMPALA_DETRAN_TABLE,
        )
        _HBase.assert_called_once_with(
            table_name=settings.HBASE_DETRAN_BASE,
            server=settings.HBASE_SERVER,
            timeout=settings.HBASE_TIMEOUT
        )
        assert resp.status_code == 200
        assert resp.json() == {"data": 1}
