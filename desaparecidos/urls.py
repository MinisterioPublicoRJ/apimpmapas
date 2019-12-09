from django.urls import path

from desaparecidos.views import DesaparecidosView


app_name = 'desaparecidos'
urlpatterns = [
    path(
        '<str:id_sinalid>',
        DesaparecidosView.as_view(),
        name='busca'
    ),
]
