from django.urls import path

from proxies.solr.views import SolrCadUnicoPessoaView, SolrPlacasView


urlpatterns = [
    path("placas", SolrPlacasView.as_view(), name="solr-placas"),
    path(
        "cadunico-pessoa",
        SolrCadUnicoPessoaView.as_view(),
        name="solr-cadunico-pessoa"
    ),
]
