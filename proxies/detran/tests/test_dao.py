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
