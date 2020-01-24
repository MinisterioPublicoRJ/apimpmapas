from django.urls import path

from .views import AlertasListView

app_name = 'dominio'

urlpatterns = [
    path(
        'dominio/alertas/<str:orgao_id>',
        AlertasListView.as_view(),
        name='lista_alertas'
    ),
]
