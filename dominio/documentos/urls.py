from django.urls import path

from dominio.documentos import views


urlpatterns = [
    path(
        "minuta-prescricao/<int:orgao_id>/<str:cpf>/<int:docu_dk>",
        views.MinutaPrescricaoView.as_view(),
        name="minuta-prescricao"
    ),
    path(
        "prorrogacao-ic/<int:orgao_id>/<str:cpf>/<int:docu_dk>",
        views.ProrrogacaoICView.as_view(),
        name="prorrogacao-ic"
    ),
    path(
        "instauracao-ic/<int:orgao_id>/<str:cpf>/<int:docu_dk>",
        views.InstauracaoICView.as_view(),
        name="instauracao-ic"
    ),
    path(
        "prorrogacao-pp/<int:orgao_id>/<str:cpf>/<int:docu_dk>",
        views.ProrrogacaoPPView.as_view(),
        name="prorrogacao-pp"
    ),
    path(
        "ros-ausentes/<int:num_delegacia>",
        views.ListaROsAusentesView.as_view(),
        name="ros-ausentes"
    ),
    path(
        "procedimentos-csmp/<int:orgao_id>/<str:cpf>",
        views.ComunicacaoCSMPView.as_view(),
        name="procedimentos-csmp"
    ),
]
