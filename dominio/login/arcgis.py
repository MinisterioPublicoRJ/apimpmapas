import requests
from django.conf import settings


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
    return resp.json()
