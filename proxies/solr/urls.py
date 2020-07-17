from django.urls import path

from proxies.solr.views import SolrPlacasView


urlpatterns = [
    path("placas", SolrPlacasView.as_view(), name="solr-placas"),
]
