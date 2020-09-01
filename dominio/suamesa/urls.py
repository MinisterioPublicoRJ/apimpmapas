from django.urls import path

from dominio.suamesa.views import (
    DocumentosDetalheView,
    SuaMesaView,
    SuaMesaDetalheView
)

urlpatterns = [
    path(
        "documentos/<str:orgao_id>",
        SuaMesaView.as_view(),
        name="suamesa-documentos",
    ),
    path(
        "documentos-detalhe/<str:orgao_id>",
        SuaMesaDetalheView.as_view(),
        name="suamesa-documentos-detalhe",
    ),
    path(
        "documentos/documento/<str:num_mprj>",
        DocumentosDetalheView.as_view(),
        name="suamesa-documentos-documento",
    )
]
