from django.urls import path

from .views import (
    PIPComparadorRadaresView,
    PIPIndicadoresDeSucessoView,
    PIPRadarPerformanceView,
    PIPPrincipaisInvestigadosView,
    PIPPrincipaisInvestigadosListaView,
)


urlpatterns = [
    path(
        "radar-performance/<str:orgao_id>",
        PIPRadarPerformanceView.as_view(),
        name="pip-radar-performance",
    ),
    path(
        "principais-investigados/<str:orgao_id>/<str:cpf>",
        PIPPrincipaisInvestigadosView.as_view(),
        name="pip-principais-investigados",
    ),
    path(
        "indicadores-sucesso/<str:orgao_id>",
        PIPIndicadoresDeSucessoView.as_view(),
        name="pip-indicadores-sucesso",
    ),
    path(
        "principais-investigados-lista/<str:representante_dk>",
        PIPPrincipaisInvestigadosListaView.as_view(),
        name="pip-principais-investigados-lista",
    ),
    path(
        "comparador-radares/<str:orgao_id>",
        PIPComparadorRadaresView.as_view(),
        name="pip-comparador-radares",
    ),
]
