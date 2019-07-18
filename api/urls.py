from django.urls import path

from api.views import EntidadeView, TipoEntidadeView, DadoView


app_name = 'api'

urlpatterns = [
    path(
        '<str:entity_type>/<str:domain_id>',
        EntidadeView.as_view(),
        name='detail_entidade'
    ),
    path(
        'ent/<str:entity_type>/<str:domain_id>',
        TipoEntidadeView.as_view(),
        name='detail_tipo_entidade'
    ),
    path(
        'data/<str:entity_type>/<str:domain_id>/<int:pk>',
        DadoView.as_view(),
        name='detail_dado'
    ),
]
