import requests
from django.conf import settings


ARCGIS_TOKEN_CACHE_KEY = "arcgis_token_key"


def get_token():
    payload = {
        "username": settings.ARCGIS_TOKEN_USERNAME,
        "password": settings.ARCGIS_TOKEN_PASSWORD,
        "f": settings.ARCGIS_TOKEN_FORMAT,
        "expiration": settings.ARCGIS_TOKEN_EXPIRATION,
        "client": settings.ARCGIS_TOKEN_CLIENT,
        "referer": settings.ARCGIS_TOKEN_REFERER,
        "ip": settings.ARCGIS_TOKEN_IP,
    }
    resp = requests.post(
        settings.ARCGIS_TOKEN_ENDPOINT,
        data=payload,
        verify=False
    )
    # TODO: raise exception if token is not returned
    return resp.json()
