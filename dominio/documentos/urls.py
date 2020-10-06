from django.urls import path

from dominio.documentos import views


urlpatterns = [
    path(
        "minuta-prescricao/<int:orgao_id>/<str:cpf>/<int:docu_dk>",
        views.MinutaPrescricaoView.as_view(),
        name="minuta-prescricao"
    ),
]
