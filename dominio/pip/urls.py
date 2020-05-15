from django.urls import path

from .views import (
    PIPDetalheAproveitamentosView,
    PIPInvestigacoesCursoAISP,
    PIPRadarPerformanceView,
    PIPVistasAbertasMensal,
    PIPPrincipaisInvestigadosView,
    PIPPrincipaisInvestigadosListaView,
)


urlpatterns = [
    path(
        "aproveitamentos/<str:orgao_id>",
        PIPDetalheAproveitamentosView.as_view(),
        name="pip-aproveitamentos",
    ),
    path(
        "aberturas-mensal/<str:orgao_id>/<str:cpf>",
        PIPVistasAbertasMensal.as_view(),
        name="pip-aberturas-mensal",
    ),
    path(
        "aisp/investigacoes/<str:orgao_id>",
        PIPInvestigacoesCursoAISP.as_view(),
        name="pip-aisp-investigacoes",
    ),
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
        "principais-investigados-lista/<str:representante_dk>",
        PIPPrincipaisInvestigadosListaView.as_view(),
        name="pip-principais-investigados-lista",
    ),
]
