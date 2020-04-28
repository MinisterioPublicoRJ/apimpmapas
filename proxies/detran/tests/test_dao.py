from unittest import mock

import pytest
from django.conf import settings

from proxies.detran.dao import DataTrafficController, HBaseGate, ImpalaGate
from proxies.exceptions import (
    DataDoesNotExistException,
    DetranAPIClientError,
    WaitDBException,
)


class TestDataTrafficControlle:
    def test_create_cache_key(self):
        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        cache_key = data_controller.cache_key
        expected = "detran_request_line_12345"

        assert cache_key == expected

    @mock.patch("proxies.detran.dao.cache")
    def test_check_request_inserted_in_queue(self, _cache):
        """
        Check in the cache if a RG was already requested
        """
        _cache.get.return_value = None
        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        request_inserted_in_queue = data_controller.check_request_queue()

        assert request_inserted_in_queue
        _cache.set.assert_called_once_with(
            data_controller.cache_key,
            True
        )

    @mock.patch("proxies.detran.dao.cache")
    def test_check_request_already_in_queue(self, _cache):
        """
        Check in the cache if a RG was already requested
        """
        _cache.get.return_value = True
        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        request_inserted_in_queue = data_controller.check_request_queue()

        assert not request_inserted_in_queue
        _cache.set.assert_not_called()


    @mock.patch("proxies.detran.dao.request_detran_data")
    def test_dispatch_request_to_detran(self, _detran_client):
        detran_data = {"id": 6789}
        _detran_client.return_value = detran_data
        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        data = data_controller.dispatch_request()

        assert data == detran_data
        _detran_client.assert_called_once_with(data_controller.rg)

    @mock.patch("proxies.detran.dao.cache")
    @mock.patch("proxies.detran.dao.request_detran_data")
    def test_remove_cache_if_dispatch_raises_exception(
            self, _detran_client, _cache):

        _detran_client.side_effect = DetranAPIClientError
        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        with pytest.raises(DetranAPIClientError):
            data_controller.dispatch_request()

        _detran_client.assert_called_once_with(data_controller.rg)
        _cache.delete.assert_called_once_with(data_controller.cache_key)

    @mock.patch.object(DataTrafficController, "persist_photo")
    @mock.patch.object(DataTrafficController, "check_request_queue")
    @mock.patch.object(DataTrafficController, "dispatch_request")
    def test_check_cache_and_send_request(
        self, _dispatch_request, _check_request_queue, _persist_photo
    ):
        """
        Execute cache check and request sending process

        """
        detran_data = {"id": 6789}
        _check_request_queue.return_value = True
        _dispatch_request.return_value = detran_data
        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        data = data_controller.request_photo()

        _check_request_queue.assert_called_once_with()
        _dispatch_request.assert_called_once_with()
        _persist_photo.assert_called_once_with(data)
        assert data == detran_data

    @mock.patch.object(DataTrafficController, "wait_for_photo")
    @mock.patch.object(DataTrafficController, "check_request_queue")
    def test_check_cache_and_wait_for_photo_in_database(
        self, _check_request_queue, _wait_for_photo
    ):
        """
        Execute cache check and request sending process

        """
        db_data = {"foto": 6789}
        _check_request_queue.return_value = False
        _wait_for_photo.return_value = db_data
        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        data = data_controller.request_photo()

        _check_request_queue.assert_called_once_with()
        _wait_for_photo.assert_called_once_with()
        assert data == db_data

    @mock.patch("proxies.detran.dao.sleep")
    @mock.patch.object(DataTrafficController, "get_db_photo")
    def test_wait_and_request_photo_from_db_sucess(
            self, _get_db_photo, _sleep):
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
            self, _get_db_photo, _sleep):
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
    def test_get_entire_data_from_db_but_it_does_not_exist(self, _get_db_data):
        _get_db_data.return_value = ()

        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        with pytest.raises(DataDoesNotExistException):
            data_controller.get_data()

        _get_db_data.assert_called_once_with()

    @mock.patch.object(DataTrafficController, "serialize")
    @mock.patch.object(DataTrafficController, "request_photo")
    @mock.patch.object(DataTrafficController, "get_db_photo")
    @mock.patch.object(DataTrafficController, "get_db_data")
    def test_get_entire_data_from_db_and_search_photo(
        self, _get_db_data, _get_db_photo, _request_photo, _serialize
    ):
        _get_db_data.return_value = {"rg": "12345"}
        _serialize.return_value = {"ser_data": 1}
        _get_db_photo.return_value = ()
        _request_photo.return_value = "b64_img"

        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        data = data_controller.get_data()
        expected_data = {"ser_data": 1, "photo": "b64_img"}

        _get_db_data.assert_called_once_with()
        _serialize.assert_called_once_with({"rg": "12345"})
        _get_db_photo.assert_called_once_with()
        _request_photo.assert_called_once_with()
        assert data == expected_data

    @mock.patch.object(DataTrafficController, "serialize")
    @mock.patch.object(DataTrafficController, "request_photo")
    @mock.patch.object(DataTrafficController, "get_db_photo")
    @mock.patch.object(DataTrafficController, "get_db_data")
    def test_get_entire_data_from_already_with_photo(
        self, _get_db_data, _get_db_photo, _request_photo, _serialize
    ):
        _get_db_data.return_value = {"rg": "12345"}
        _serialize.return_value = {"ser_data": 1}
        _get_db_photo.return_value = "b64_img"

        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        data = data_controller.get_data()
        expected_data = {"ser_data": 1, "photo": "b64_img"}

        _get_db_data.assert_called_once_with()
        _serialize.assert_called_once_with({"rg": "12345"})
        _get_db_photo.assert_called_once_with()
        _request_photo.assert_not_called()
        assert data == expected_data

    @mock.patch("proxies.detran.dao.HBaseGate")
    def test_select_photo_from_db(self, _HBaseGate):
        db_mock = mock.Mock()
        _HBaseGate.return_value = db_mock

        rg = "123456"
        data_controller = DataTrafficController(rg=rg, photo_dao=db_mock)
        data_controller.get_db_photo()

        db_mock.select.assert_called_once_with(
            row_id=rg,
            columns=[data_controller.photo_column],
        )

    def test_calculate_image_md5_hash(self):
        rg = "12345"
        data_controller = DataTrafficController(rg=rg)
        photo = "b64_img"

        hash_md5 = data_controller.md5_hash(photo)
        expected = "dd8bbfe65432d2cfd49b8bc239bc590e"

        assert hash_md5 == expected

    @mock.patch("proxies.detran.dao.cache")
    @mock.patch.object(DataTrafficController, "md5_hash")
    @mock.patch("proxies.detran.dao.HBaseGate")
    def test_insert_photo_in_db(self, _HBaseGate, _md5_hash, _cache):
        db_mock = mock.Mock()
        _HBaseGate.return_value = db_mock
        _md5_hash.return_value = "photo_hash"

        rg = "123456"
        data_controller = DataTrafficController(rg=rg, photo_dao=db_mock)
        photo = "b64_img"
        data_controller.persist_photo(photo)

        db_mock.insert.assert_called_once_with(
            row_id=rg,
            data={
                data_controller.photo_column: photo,
                data_controller.hash_column: "photo_hash",
            }
        )
        _cache.delete.assert_called_once_with(data_controller.cache_key)

    @mock.patch("proxies.detran.dao.ImpalaGate")
    def test_select_data_from_impala(self, _ImpalaGate):
        db_mock = mock.Mock()
        _ImpalaGate.return_value = db_mock

        rg = "123456"
        data_controller = DataTrafficController(rg=rg, data_dao=db_mock)
        data_controller.get_db_data()

        db_mock.select.assert_called_once_with(
            columns=["*"],
            parameters={data_controller.db_key: data_controller.rg}
        )

    @mock.patch("proxies.detran.dao.DetranSerializer")
    def test_serialize_result_set(self, _DetranSerializer):
        data_mock = mock.Mock()
        data_mock.data = {"data": 1}
        _DetranSerializer.return_value = data_mock

        result_set = (1, 2)
        data_controller = DataTrafficController(rg="12345")
        ser_data = data_controller.serialize(result_set)

        _DetranSerializer.assert_called_once_with(result_set)
        assert ser_data == {"data": 1}


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
            settings.HBASE_SERVER, timeout=settings.HBASE_TIMEOUT,
        )
        connection_mock.table.assert_called_once_with(table_name)
        assert table == "table obj"

    def test_select_row(self):
        table_mock = mock.Mock()
        row_id = "12345"
        column_names = ["col1", "col2"]
        with mock.patch(
            "proxies.detran.dao.HBaseGate.get_table",
            new_callable=mock.PropertyMock
        ) as _get_table:
            _get_table.return_value = table_mock
            db_gate = HBaseGate(table_name="table_name")
            db_gate.select(row_id, column_names)

        table_mock.row.assert_called_once_with(row_id, columns=column_names)

    def test_insert_row(self):
        table_mock = mock.Mock()
        row_id = "12345"
        data = {"col1": "val1", "col2": "val2"}
        with mock.patch(
            "proxies.detran.dao.HBaseGate.get_table",
            new_callable=mock.PropertyMock
        ) as _get_table:
            _get_table.return_value = table_mock
            db_gate = HBaseGate(table_name="table_name")
            db_gate.insert(row_id, data)

        table_mock.put.assert_called_once_with(row_id, data=data)


class TestImpalaGate:
    @mock.patch("proxies.detran.dao.impala_execute")
    def test_select_from_db(self, _impala_execute):
        result_set = (1, 2)
        _impala_execute.return_value = result_set
        table_name = "schema.table"
        parameters = {"par_1": "value_1"}
        impala_obj = ImpalaGate(table_name=table_name)
        cols = ["*"]
        data = impala_obj.select(cols, parameters)

        _impala_execute.assert_called_once_with(
            "SELECT * FROM schema.table WHERE par_1 = :par_1",
            {"par_1": "value_1"},
        )
        assert data == result_set
