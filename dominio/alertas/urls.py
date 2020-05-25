from django.urls import path

from .views import AlertasView, ResumoAlertasView


urlpatterns = [
    path('<str:orgao_id>', AlertasView.as_view(), name='lista_alertas'),
    path(
        'list/<str:orgao_id>',
        ResumoAlertasView.as_view(),
        name='resumo_alertas'
    ),
]
