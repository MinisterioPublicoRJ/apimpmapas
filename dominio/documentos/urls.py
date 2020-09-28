from django.urls import path

from dominio.documentos import views


urlpatterns = [
    path(
        "minuta-prescricao/<docu_dk>",
        views.MinutaPrescricaoView.as_view(),
        name="minuta-prescricao"
    ),
]
