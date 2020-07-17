from django.urls import include, path

from proxies.login.views import (
    SCAJSONWebRefreshTokenAPIView,
    SCAJSONWebTokenAPIView,
)

app_name = "proxies"
urlpatterns = [
    path("token/", SCAJSONWebTokenAPIView.as_view()),
    path("token-refresh/", SCAJSONWebRefreshTokenAPIView.as_view()),
    path("solr/", include("proxies.solr.urls")),
    path("", include("proxies.detran.urls")),
]
