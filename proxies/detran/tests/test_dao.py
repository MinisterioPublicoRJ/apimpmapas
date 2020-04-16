from unittest import mock

from proxies.detran.dao import DataTrafficController


def test_create_cache_key():
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    cache_key = data_controller.cache_key
    expected = "detran_request_line_12345"

    assert cache_key == expected


@mock.patch("proxies.detran.dao.cache")
def test_get_or_set_from_cache(_cache):
    """
    Check in the cache if a RG was already requested
    """
    _cache.get_or_set.return_value = None
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    request_awaiting = data_controller.get_or_set_cache()

    assert not request_awaiting
    _cache.get_or_set.assert_called_once_with(data_controller.cache_key, True)


@mock.patch("proxies.detran.dao.cache")
@mock.patch("proxies.detran.dao.request_detran_data")
def test_dispatch_request_to_detran(_detran_client, _cache):
    detran_data = {"id": 6789}
    _detran_client.return_value = detran_data
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    data = data_controller.dispatch_request()

    assert data == detran_data
    _detran_client.assert_called_once_with(data_controller.rg)
    _cache.delete.assert_called_once_with(data_controller.cache_key)


@mock.patch.object(DataTrafficController, "get_or_set_cache")
@mock.patch.object(DataTrafficController, "dispatch_request")
def test_check_cache_and_send_request(_dispatch_request, _get_or_set_cache):
    """
    Execute cache check and request sending process

    """
    detran_data = {"id": 6789}
    _get_or_set_cache.return_value = None
    _dispatch_request.return_value = detran_data
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    data = data_controller.get_data()

    _get_or_set_cache.assert_called_once_with()
    _dispatch_request.assert_called_once_with()
    assert data == detran_data
