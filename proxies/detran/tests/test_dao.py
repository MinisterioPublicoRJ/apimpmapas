from proxies.detran.dao import DataTrafficController


def test_create_cache_key():
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    cache_key = data_controller.cache_key
    expected = "detran_request_line_12345"

    assert cache_key == expected


def _test_check_if_a_request_is_already_in_cache():
    """
    Check in the cache if a RG was already requested
    """
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
