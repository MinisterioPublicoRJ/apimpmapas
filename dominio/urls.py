from django.urls import path

from .views import AcervoView, AcervoVariationView  # , AlertasListView

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
    path(
        'acervo_variation/<str:orgao_id>/<str:tipo_acervo>/<str:dt_inicio>/<str:dt_fim>',
        AcervoVariationView.as_view(),
        name='acervo_variation'
    )
]
