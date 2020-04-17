from unittest import mock

import pytest
from django.conf import settings

from proxies.detran.dao import DataTrafficController, HBaseGate
from proxies.exceptions import DataDoesNotExistException, WaitDBException


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


@mock.patch.object(DataTrafficController, "persist_photo")
@mock.patch.object(DataTrafficController, "get_or_set_cache")
@mock.patch.object(DataTrafficController, "dispatch_request")
def test_check_cache_and_send_request(
        _dispatch_request, _get_or_set_cache, _persist_photo):
    """
    Execute cache check and request sending process

    """
    detran_data = {"id": 6789}
    _get_or_set_cache.return_value = None
    _dispatch_request.return_value = detran_data
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    data = data_controller.request_photo()

    _get_or_set_cache.assert_called_once_with()
    _dispatch_request.assert_called_once_with()
    _persist_photo.assert_called_once_with(data)
    assert data == detran_data


@mock.patch.object(DataTrafficController, "wait_for_photo")
@mock.patch.object(DataTrafficController, "get_or_set_cache")
def test_check_cache_and_wait_for_photo_in_database(
        _get_or_set_cache, _wait_for_photo):
    """
    Execute cache check and request sending process

    """
    db_data = {"foto": 6789}
    _get_or_set_cache.return_value = True
    _wait_for_photo.return_value = db_data
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    data = data_controller.request_photo()

    _get_or_set_cache.assert_called_once_with()
    _wait_for_photo.assert_called_once_with()
    assert data == db_data


@mock.patch("proxies.detran.dao.sleep")
@mock.patch.object(DataTrafficController, "get_db_photo")
def test_wait_and_request_photo_from_db_sucess(_get_db_photo, _sleep):
    """
    Execute cache check and request sending process

    """
    db_data = {"foto": 6789}
    empty_result = ()
    _get_db_photo.side_effect = [empty_result, db_data]
    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    data = data_controller.wait_for_photo()

    sleep_calls = [
        mock.call(data_controller.wait_time),
        mock.call(data_controller.wait_time),
    ]
    get_db_photo_calls = [mock.call(), mock.call()]

    _sleep.assert_has_calls(sleep_calls)
    _get_db_photo.assert_has_calls(get_db_photo_calls)
    assert data == db_data


@mock.patch("proxies.detran.dao.sleep")
@mock.patch.object(DataTrafficController, "get_db_photo")
def test_wait_and_request_photo_from_db_exceed_max_attemps(
        _get_db_photo, _sleep):
    """
    Execute cache check and request sending process

    """
    empty_result = ()
    _get_db_photo.side_effect = [empty_result, empty_result]
    rg = "12345"
    data_controller = DataTrafficController(rg=rg, max_attempts=2)

    with pytest.raises(WaitDBException):
        data_controller.wait_for_photo()

    sleep_calls = [
        mock.call(data_controller.wait_time),
        mock.call(data_controller.wait_time),
    ]
    get_db_photo_calls = [mock.call(), mock.call()]

    _sleep.assert_has_calls(sleep_calls)
    _get_db_photo.assert_has_calls(get_db_photo_calls)


@mock.patch.object(DataTrafficController, "get_db_data")
def test_get_entire_data_from_db_but_it_does_not_exist(_get_db_data):
    _get_db_data.return_value = ()

    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    with pytest.raises(DataDoesNotExistException):
        data_controller.get_data()

    _get_db_data.assert_called_once_with()


@mock.patch.object(DataTrafficController, "request_photo")
@mock.patch.object(DataTrafficController, "get_db_photo")
@mock.patch.object(DataTrafficController, "get_db_data")
def test_get_entire_data_from_db_and_search_photo(
        _get_db_data, _get_db_photo, _request_photo):
    _get_db_data.return_value = {"rg": "12345"}
    _get_db_photo.return_value = ()
    _request_photo.return_value = "b64_img"

    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    data = data_controller.get_data()
    expected_data = {"rg": rg, "photo": "b64_img"}

    _get_db_data.assert_called_once_with()
    _get_db_photo.assert_called_once_with()
    _request_photo.assert_called_once_with()
    assert data == expected_data


@mock.patch.object(DataTrafficController, "request_photo")
@mock.patch.object(DataTrafficController, "get_db_photo")
@mock.patch.object(DataTrafficController, "get_db_data")
def test_get_entire_data_from_already_with_photo(
        _get_db_data, _get_db_photo, _request_photo):
    _get_db_data.return_value = {"rg": "12345"}
    _get_db_photo.return_value = "b64_img"

    rg = "12345"
    data_controller = DataTrafficController(rg=rg)
    data = data_controller.get_data()
    expected_data = {"rg": rg, "photo": "b64_img"}

    _get_db_data.assert_called_once_with()
    _get_db_photo.assert_called_once_with()
    _request_photo.assert_not_called()
    assert data == expected_data


class TestHBaseGate:
    @mock.patch("proxies.detran.dao.HBaseConnection")
    def test_get_table(self, _Connection):
        connection_mock = mock.Mock()
        connection_mock.table.return_value = "table obj"
        _Connection.return_value = connection_mock

        table_name = "table_name"
        db_gate = HBaseGate(table_name=table_name)
        table = db_gate.get_table

        _Connection.assert_called_once_with(
            settings.HBASE_SERVER,
            timeout=settings.HBASE_TIMEOUT,
        )
        connection_mock.table.assert_called_once_with(table_name)
        assert table == "table obj"
