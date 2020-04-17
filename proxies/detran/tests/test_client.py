import pytest

from proxies.detran import client

def test_get_photo_rg():
    rg = "12345"
    photo = client.request
    expected = "ThisIsAPhoto,TrustMe"

    assert client.request_data(rg) == expected
