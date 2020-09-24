from django.urls import path

from dominio.suamesa.views import SuaMesaView, SuaMesaDetalheView

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
    ),]
