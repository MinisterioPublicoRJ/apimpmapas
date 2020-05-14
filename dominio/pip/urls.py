from django.urls import path

from .views import (
    PIPDetalheAproveitamentosView,
    PIPSuaMesaInvestigacoesAISPView,
    PIPSuaMesaInqueritosView,
    PIPSuaMesaPICsView,
    PIPRadarPerformanceView,
    PIPVistasAbertasMensalView,
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
        PIPVistasAbertasMensalView.as_view(),
        name="pip-aberturas-mensal",
    ),
    path(
        "suamesa/investigacoes-aisp/<str:orgao_id>",
        PIPSuaMesaInvestigacoesAISPView.as_view(),
        name="pip-suamesa-investigacoes-aisp",
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
