from unittest import mock

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from proxies.exceptions import (
    DataDoesNotExistException,
    DetranAPIClientError,
    WaitDBException,
)


TEST_TOKEN = "simple-token"


@override_settings(SIMPLE_AUTH_TOKEN=TEST_TOKEN)
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

        # View must remove padding zero
        rg = "012345"
        url = reverse("proxies:foto-detran", kwargs={"rg": rg})
        resp = self.client.get(url, {"proxy-token": TEST_TOKEN})
        expected_used_rg = str(int(rg))

        _DataController.assert_called_once_with(
            rg=expected_used_rg,
            data_dao=_Impala.return_value,
            photo_dao=_HBase.return_value,
        )
        _Impala.assert_called_once_with(
            table_name=settings.EXADATA_DETRAN_DATA_ORIGIN,
        )
        _HBase.assert_called_once_with(
            table_name=settings.EXADATA_DETRAN_PHOTO_ORIGIN,
            server=settings.HBASE_SERVER,
            timeout=settings.HBASE_TIMEOUT,
        )
        assert resp.status_code == 200
        assert resp.json() == {"data": 1}

    @mock.patch("proxies.detran.views.DataTrafficController")
    def test_exception_detran_api(self, _DataController):
        controller_mock = mock.Mock()
        controller_mock.get_data.side_effect = DetranAPIClientError
        _DataController.return_value = controller_mock

        rg = "12345"
        url = reverse("proxies:foto-detran", kwargs={"rg": rg})
        resp = self.client.get(url, {"proxy-token": TEST_TOKEN})

        assert resp.status_code == 503

    @mock.patch("proxies.detran.views.DataTrafficController")
    def test_data_do_not_exist(self, _DataController):
        controller_mock = mock.Mock()
        controller_mock.get_data.side_effect = DataDoesNotExistException
        _DataController.return_value = controller_mock

        rg = "12345"
        url = reverse("proxies:foto-detran", kwargs={"rg": rg})
        resp = self.client.get(url, {"proxy-token": TEST_TOKEN})

        assert resp.status_code == 404
        assert resp.json() == {"detail": f"Dado não encontrado para RG: {rg}"}

    @mock.patch("proxies.detran.views.DataTrafficController")
    def test_wait_database_exception(self, _DataController):
        controller_mock = mock.Mock()
        controller_mock.get_data.side_effect = WaitDBException
        _DataController.return_value = controller_mock

        rg = "12345"
        url = reverse("proxies:foto-detran", kwargs={"rg": rg})
        resp = self.client.get(url, {"proxy-token": TEST_TOKEN})

        assert resp.status_code == 503
        assert resp.json() == {
            "detail": "Tempo de busca dos dados excedeu o tempo máximo"
        }

    @override_settings(SIMPLE_AUTH_TOKEN="very-secure-token")
    def test_no_token_permission_denied(self):
        rg = "12345"
        url = reverse("proxies:foto-detran", kwargs={"rg": rg})
        resp = self.client.get(url)

        assert resp.status_code == 403

    @override_settings(SIMPLE_AUTH_TOKEN="even-more-secure-token")
    @mock.patch("proxies.detran.views.DataTrafficController")
    def test_with_token_permission_granted(self, _DataController):
        _DataController.return_value.get_data.return_value = {"data": 1}
        rg = "12345"
        url = reverse("proxies:foto-detran", kwargs={"rg": rg})
        resp = self.client.get(url, {"proxy-token": "even-more-secure-token"})

        assert resp.status_code == 200
        assert resp.data == {"data": 1}
