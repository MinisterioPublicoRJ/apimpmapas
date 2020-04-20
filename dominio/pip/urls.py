from django.urls import path

from .views import (
    PIPDetalheAproveitamentosView,
    PIPVistasAbertasMensal,
    PIPInvestigacoesCursoAISP,
)


urlpatterns = [
    path(
        "aproveitamentos/<str:orgao_id>",
        PIPDetalheAproveitamentosView.as_view(),
        name="pip-aproveitamentos"
    ),
    path(
        "aberturas-mensal/<str:orgao_id>/<str:cpf>",
        PIPVistasAbertasMensal.as_view(),
        name="pip-aberturas-mensal"
    ),
    path(
        "aisp/investigacoes/<str:orgao_id>",
        PIPInvestigacoesCursoAISP.as_view(),
        name="pip-aisp-investigacoes"
    ),
]
