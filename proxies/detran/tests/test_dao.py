from unittest import mock

from proxies.detran.dao import DataTrafficController


def test_create_cache_key():
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    cache_key = data_controller.cache_key
    expected = "detran_request_line_12345"

    assert cache_key == expected


@mock.patch("proxies.detran.dao.cache")
def test_request_is_not_in_cache_yet(_cache):
    """
    Check in the cache if a RG was already requested
    """
    _cache.get.return_value = None
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    request_awaiting = data_controller.request_awaiting

    assert not request_awaiting
    _cache.get.assert_called_once_with(data_controller.cache_key)


@mock.patch("proxies.detran.dao.cache")
def test_request_is_already_in_cache(_cache):
    """
    Check in the cache if a RG was already requested
    """
    _cache.get.return_value = True
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    request_awaiting = data_controller.request_awaiting

    assert request_awaiting
    _cache.get.assert_called_once_with(data_controller.cache_key)
