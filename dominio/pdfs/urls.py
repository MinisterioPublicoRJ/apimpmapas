from django.urls import path

from dominio.pdfs.views import ItGateView


urlpatterns = [
    path(
        "gate/<str:it_gate_id>",
        ItGateView.as_view(),
        name="pdfs-itgate",
    )
]
