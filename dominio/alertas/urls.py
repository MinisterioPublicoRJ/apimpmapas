from django.urls import path

from .views import AlertasView, ResumoAlertasView, AlertasComprasView


urlpatterns = [
    path('<str:orgao_id>', AlertasView.as_view(), name='lista_alertas'),
    path(
        'list/<str:orgao_id>',
        ResumoAlertasView.as_view(),
        name='resumo_alertas'
    ),
    path(
        'compras/<str:orgao_id>',
        AlertasComprasView.as_view(),
        name='compras_alertas'
    ),
]
