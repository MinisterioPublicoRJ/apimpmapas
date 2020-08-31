from django.urls import path

from dominio.alertas import views


urlpatterns = [
    path('<str:orgao_id>', views.AlertasView.as_view(), name='lista_alertas'),
    path(
        'list/<str:orgao_id>',
        views.ResumoAlertasView.as_view(),
        name='resumo_alertas'
    ),
    path(
        "dispensar/<str:orgao_id>/<str:sigla>",
        views.DispensarAlertaView.as_view(),
        name="dispensar_alerta"
    ),
    path(
        'compras/<str:orgao_id>',
        views.AlertasComprasView.as_view(),
        name='compras_alertas'
    ),
]
