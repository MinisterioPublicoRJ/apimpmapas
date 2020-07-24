from django.conf import settings
from django.core.cache import cache

from dominio.login.arcgis import ARCGIS_TOKEN_CACHE_KEY, get_token
from mprj_api.celeryconfig import app


@app.task
def renew_arcgis_token():
    print("running")
    resp = get_token()
    cache.set(
        ARCGIS_TOKEN_CACHE_KEY,
        resp,
        timeout=settings.ARCGIS_TOKEN_EXPIRATION * 60
    )
