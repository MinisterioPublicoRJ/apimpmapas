from django.urls import path

from .views import (
    SaidasView,
    EntradasView,
    AcervoVariationView,
    AcervoVariationTopNView,
    OutliersView  # , AlertasListView
)

app_name = 'dominio'

urlpatterns = [
    # path(
    #     'dominio/alertas/<str:orgao_id>',
    #     AlertasListView.as_view(),
    #     name='lista_alertas'
    # ),
    path(
        'acervo_variation/'
        '<str:orgao_id>/<str:dt_inicio>/<str:dt_fim>',
        AcervoVariationView.as_view(),
        name='acervo_variation'
    ),
    path(
        'acervo_variation_topn/'
        '<str:orgao_id>/<str:dt_inicio>/<str:dt_fim>/<str:n>',
        AcervoVariationTopNView.as_view(),
        name='acervo_variation_topn'
    ),
    path(
        'outliers/'
        '<str:orgao_id>/<str:dt_calculo>',
        OutliersView.as_view(),
        name='outliers'
    ),
    path(
        'saidas/<str:orgao_id>',
        SaidasView.as_view(),
        name='saidas'
    ),
    path(
        'entradas/<str:orgao_id>/<str:cod_matricula>',
        EntradasView.as_view(),
        name='entradas'
    )
]
