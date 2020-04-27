from django.urls import path

from proxies.detran.views import FotoDetranView


urlpatterns = [
    path("foto-detran/<str:rg>", FotoDetranView.as_view(), name="foto-detran"),
]
