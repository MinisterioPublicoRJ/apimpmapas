from django.urls import path

from .views import EntidadeView, DadoView


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
]
