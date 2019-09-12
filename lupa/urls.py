from django.urls import path

from .views import (
    EntidadeView,
    DadoView,
    OsmQueryView
)


app_name = 'lupa'

urlpatterns = [
    path(
        '<str:entity_type>/<str:domain_id>',
        EntidadeView.as_view(),
        name='detail_entidade'
    ),
    path(
        '<str:entity_type>/<str:domain_id>/<int:pk>',
        DadoView.as_view(),
        name='detail_dado'
    ),
    path(
        'search/mapsearch/<str:terms>',
        OsmQueryView.as_view(),
        name="mapsearch"
    ),
]
