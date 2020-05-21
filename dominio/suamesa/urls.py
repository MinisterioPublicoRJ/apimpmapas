from django.urls import path

from dominio.suamesa.views import SuaMesaView


urlpatterns = [
    path(
        "documentos/<str:orgao_id>",
        SuaMesaView.as_view(),
        name="suamesa-documentos",
    )
]
