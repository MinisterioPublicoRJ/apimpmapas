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
        "dispensar/<str:orgao_id>/<str:alerta_id>",
        views.DispensarAlertaView.as_view(),
        name="dispensar_alerta"
    ),
    path(
        "retornar/<str:orgao_id>/<str:alerta_id>",
        views.RetornarAlertaView.as_view(),
        name="retornar_alerta"
    ),
    path(
        "ouvidoria/<str:orgao_id>/<str:sigla_alerta>/<str:alerta_id>",
        views.EnviarAlertaOuvidoriaView.as_view(),
        name="alerta_ouvidoria"
    ),
    path(
        'compras/<str:orgao_id>',
        views.AlertasComprasView.as_view(),
        name='compras_alertas'
    ),
    path(
        'overlay/<str:docu_dk>',
        views.AlertasOverlayView.as_view(),
        name='overlay_alertas'
    ),
    path(
        'baixar/<str:orgao_id>',
        views.BaixarAlertasView.as_view(),
        name='baixar_alertas'
    )
]
