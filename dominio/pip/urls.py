from django.urls import path

from .views import (
    PIPDetalheAproveitamentosView,
    PIPInvestigacoesCursoAISP,
    PIPSuaMesaInqueritosView,
    PIPSuaMesaPICsView,
    PIPRadarPerformanceView,
    PIPVistasAbertasMensal,
    PIPPrincipaisInvestigadosView,
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
        "suamesa/inqueritos/<str:orgao_id>",
        PIPSuaMesaInqueritosView.as_view(),
        name="pip-suamesa-inqueritos",
    ),
    path(
        "suamesa/pics/<str:orgao_id>",
        PIPSuaMesaPICsView.as_view(),
        name="pip-suamesa-pics",
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
]
