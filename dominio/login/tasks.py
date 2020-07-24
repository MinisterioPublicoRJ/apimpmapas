from django.conf import settings
from django.core.cache import cache

from dominio.login.arcgis import ARCGIS_TOKEN_CACHE_KEY, get_token
from mprj_api.celeryconfig import app


@app.task(
    autoretry_for=(Exception,), retry_kwargs={"max_retries": 5, "countdown": 2}
)
def renew_arcgis_token():
    resp = get_token()
    cache.set(
        ARCGIS_TOKEN_CACHE_KEY,
        resp,
        timeout=settings.ARCGIS_TOKEN_EXPIRATION * 60,
    )
