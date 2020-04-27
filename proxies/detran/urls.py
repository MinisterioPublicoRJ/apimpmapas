from django.urls import path

from proxies.detran.views import foto_detran_view


urlpatterns = [
    path("foto-detran/<str:rg>", foto_detran_view, name="foto-detran"),
]
