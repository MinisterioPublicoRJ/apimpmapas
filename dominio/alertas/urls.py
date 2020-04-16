from django.urls import path

from .views import AlertasView


urlpatterns = [
    path('<str:orgao_id>', AlertasView.as_view(), name='lista_alertas'),
]
