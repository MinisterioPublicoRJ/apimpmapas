from django.urls import path

from .views import AcervoView  # , AlertasListView

app_name = 'dominio'

urlpatterns = [
    # path(
    #     'dominio/alertas/<str:orgao_id>',
    #     AlertasListView.as_view(),
    #     name='lista_alertas'
    # ),
    path(
        'acervo/<str:orgao_id>/<str:tipo_acervo>/<str:data>',
        AcervoView.as_view(),
        name='acervo'
    ),
]
