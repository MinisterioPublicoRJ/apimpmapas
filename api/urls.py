from django.urls import path

from api.views import EntidadeView


app_name = 'api'

urlpatterns = [
    path(
        '<str:entity_type>/<str:domain_id>',
        EntidadeView.as_view(),
        name='detail_entidade'
    ),
]
