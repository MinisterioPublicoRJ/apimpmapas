from django.urls import path

from .views import (
    EntidadeView,
    DadoDetalheView,
    DadoEntidadeView,
    OsmQueryView,
    GeoSpatialQueryView
)


app_name = 'lupa'

urlpatterns = [
    path(
        'entidade/<str:entity_type>/<str:domain_id>',
        EntidadeView.as_view(),
        name='detail_entidade'
    ),
    path(
        'dado/<str:entity_type>/<str:domain_id>/<int:pk>',
        DadoEntidadeView.as_view(),
        name='detail_dado'
    ),
    path(
        'detalhe/<str:entity_type>/<str:domain_id>/<int:pk>',
        DadoDetalheView.as_view(),
        name='detail_detalhes'
    ),
    path(
        'search/mapsearch/<str:terms>',
        OsmQueryView.as_view(),
        name="mapsearch"
    ),
    path(
        'geospatial/entity/<str:lat>/<str:lon>/<str:value>',
        GeoSpatialQueryView.as_view(),
        name="geospatial_entity"
    ),
]
